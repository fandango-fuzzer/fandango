

<start> ::= <TimerControl:timer_start> <TimerEvent:timer_expired>

where str(<timer_start>..<timer_id>) == "1"
where str(<timer_expired>..<timer_id>) == "1"
where str(<timer_start>..<timer_timeout>) == "5"