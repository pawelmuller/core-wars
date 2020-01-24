;redcode-94
;name Blur Scanner

MOV.B	$1,	#0
ADD.AB	#4884,	#4884
MOV.I	*3,	>-2
JMZ.F	$-2,	@-2
JMN.B	$-4,	*-4
SPL.B	$0,	$0
MOV.I	$2,	>-4
DJN.F	$-1,	>-5
DAT.F	<2667,	$8