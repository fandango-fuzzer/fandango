import shlex
import subprocess
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language import DerivationTree
from fandango.language.parse import parse
from fandango.language.symbol import NonTerminal, Terminal


def is_syntactically_valid_ssl(tree):
    with open("evaluation/experiments/ssl/certificates/tmp.der", "wb") as fd:
        fd.write(tree.to_bytes("latin1"))

    command = shlex.split("openssl verify -CAfile tmp.der tmp.der")

    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc.communicate()
    return proc.returncode == 0


def evaluate_ssl():
    with open("evaluation/experiments/ssl/ssl.fan", "r") as fd:
        grammar, constraints = parse(fd)
    start_time = time.time()
    fandango = Fandango(
        grammar,
        constraints,
        logger_level=LoggerLevel.DEBUG,
        population_size=100,
        profiling=True,
    )
    fandango.evolve(max_generations=100, desired_solutions=100)
    end_time = time.time()
    sol = fandango.solution
    i = 0
    for c in sol:
        cert = insert_key(i, c)
        cert = fixlength(cert)
        tbs = find_tbs(cert)
        issuer = get_issuer(cert)
        cert = insert_issuer(cert, issuer)
        cert = fixlength(cert)
        sig = sign_certificate_chain(tbs, i)
        cert = insert_sig(cert, sig)
        cert = fixlength(cert)
        if is_syntactically_valid_ssl(cert):
            with open(
                f"evaluation/experiments/ssl/certificates/fuzzed_{i}.der", "wb"
            ) as fd:
                fd.write(bytes(str(cert), "latin1"))
            i += 1
    print(f"Generated {i} valid SSL certificates in {end_time - start_time} seconds")


def insert_issuer(tree, issuer):
    if not tree._children:
        return tree
    if tree.symbol.symbol == "<issuer>":
        tree = DerivationTree(NonTerminal("<issuer>"), issuer)
        return tree
    new_children = []
    for c in tree._children:
        new_children.append(insert_issuer(c, issuer))
    tree = DerivationTree(NonTerminal(tree.symbol.symbol), new_children)
    return tree


def get_issuer(tree):
    if tree.symbol.symbol == "<subject>":
        return tree._children
    else:
        for c in tree._children:
            tmp = get_issuer(c)
            if tmp is not None:
                return tmp
    return None


def sign_certificate_chain(tbs, i):
    key_file = f"evaluation/experiments/ssl/certificates/private_{i}.pem"
    with open(key_file, "rb") as fd:
        key = serialization.load_pem_private_key(fd.read(), password=None)
    tbs = bytes(str(tbs), "latin1")
    sig = key.sign(tbs, padding.PKCS1v15(), hashes.SHA256())
    sig = b"\x00" + sig
    return sig.decode("latin1")


def ins_key(children, tree):
    if not tree._children:
        return tree
    if tree.symbol.symbol == "<bit_string_value_pubkey>":
        tree = DerivationTree(NonTerminal("<bit_string_value_pubkey>"), children)
        return tree
    new_children = []
    for c in tree._children:
        new_children.append(ins_key(children, c))
    tree = DerivationTree(NonTerminal(tree.symbol.symbol), new_children)
    return tree


def insert_key(i, tree):

    privkey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    with open(
        "evaluation/experiments/ssl/certificates/private_" + str(i) + ".pem", "wb"
    ) as fd:
        fd.write(
            privkey.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    pubkey = privkey.public_key()

    key = bytes("\x00", "latin1") + pubkey.public_bytes(
        encoding=serialization.Encoding.DER, format=serialization.PublicFormat.PKCS1
    )
    children = []
    for c in key.decode("latin1"):
        children.append(
            DerivationTree(
                NonTerminal("<byte>"),
                [DerivationTree(Terminal(c.encode("latin1")), [])],
            )
        )

    tree = ins_key(children, tree)

    return tree


def fixlength(tree):
    if not tree._children:
        return tree

    new_children = []
    for c in tree._children:
        new_children.append(fixlength(c))

    if (
        len(new_children) == 3
        and isinstance(new_children[0].symbol.symbol, str)
        and isinstance(new_children[1].symbol.symbol, str)
    ):
        if (
            len(new_children) == 3
            and new_children[0].symbol.symbol.endswith("_tag>")
            and new_children[1].symbol.symbol.endswith("_length>")
        ):
            correct_length = len(str(new_children[2]))
            newtree = new_length_tree(correct_length)
            new_children[1] = DerivationTree(
                NonTerminal(new_children[1].symbol.symbol), [newtree]
            )

    tree = DerivationTree(NonTerminal(tree.symbol.symbol), children=new_children)
    return tree


def new_length_tree(length):
    if length < 128:
        return DerivationTree(
            NonTerminal("<length>"),
            [
                DerivationTree(
                    NonTerminal("<short_length>"),
                    [
                        DerivationTree(
                            NonTerminal("<byte0_127>"),
                            [DerivationTree(Terminal(chr(length).encode("latin1")))],
                        )
                    ],
                )
            ],
        )

    values = []
    while length:
        values.append(length & 0xFF)
        length >>= 8
    values.reverse()

    children = [
        DerivationTree(
            NonTerminal("<byte128_255>"),
            [DerivationTree(Terminal((chr(0x80 | len(values)).encode("latin1"))))],
        )
    ]

    for val in values:
        children += [
            DerivationTree(
                NonTerminal("<byte>"),
                [DerivationTree(Terminal(chr(val).encode("latin1")))],
            )
        ]

    return DerivationTree(
        NonTerminal("<length>"),
        [DerivationTree(NonTerminal("<long_length>"), children)],
    )


def find_tbs(tree):
    if tree.symbol.symbol == "<certificate>":
        return tree
    else:
        for c in tree._children:
            tmp = find_tbs(c)
            if tmp is not None:
                return tmp
    return None


def build_sig_tree(sig):
    children = []
    for c in sig:
        children.append(("<byte>", [(c, [])]))
    return DerivationTree(NonTerminal("<bit_string_value_signature>"), children)


def insert_sig(tree, sig):
    tree._children[2]._children[2]._children[2] = DerivationTree(
        NonTerminal("<bit_string_value_signature>"),
        [DerivationTree(Terminal(sig.encode("latin1")), [])],
    )
    return tree


if __name__ == "__main__":
    evaluate_ssl()
