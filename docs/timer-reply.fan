<start> ::= <In:request> <TimerControl:reply_start> <reply>
<reply> ::= <Out:response> <TimerControl:reply_cancel> | <TimerEvent:reply_expired>
<request> ::= 'PING\n'
<response> ::= 'PING\n'

<reply_start> ::= <timer_start>
<reply_cancel> ::= <timer_cancel>
<reply_expired> ::= <timer_expired>

where all(str(<t>..<timer_timeout>) == '1' for <t> in *<reply_start>)
where all(str(<s>..<timer_id>) == '1' for <s> in *<reply_start>)
where all(str(<c>..<timer_id>) == '1' for <c> in *<reply_cancel>)
where all(str(<e>..<timer_id>) == '1' for <e> in *<reply_expired>)
