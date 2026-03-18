"""Chromosome abstractions for evolutionary algorithms."""

from fandango.evolution.chromosomes.base import Chromosome
from fandango.evolution.chromosomes.individual import Individual
from fandango.evolution.chromosomes.suite import Suite

__all__ = ["Chromosome", "Individual", "Suite"]
