<start> ::= <TimerControl:wait_start> <TimerEvent:wait_expired> <StdOut:done>
<wait_start> ::= <timer_start>
<wait_expired> ::= <timer_expired>
<done> ::= 'Timer expired\n'

where str(<wait_start>..<timer_id>) == '1'
where str(<wait_start>..<timer_timeout>) == '0.5'
where str(<wait_expired>..<timer_id>) == '1'
