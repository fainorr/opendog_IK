import time

# Block 1

T0_EN = Wait || Back || TRight || SLeft
T1_EN = Forward || TLeft || SRight

# --------------------TIMER_0--------------------
A_time0 = wait_time0 && T0_EN
B_time0 = wait_time0 && !T0_EN
C_time0 = timing_time0 && !T0_EN
D_time0 = timing_time0 && T0_EN

wait_time0 = B_time0 || C_time0
timingt_time0 = A_time0 || D_time0

if (A_time0):
	Start_time0 = time.time()

if(timing_time):
	delta_t0 = time.time() - Start_time0

else:
	delta_t0 = 0

T0 = delta_t0 > 5
#-----------------------------------------------

#--------------------TIMER_1--------------------
A_time1 = wait_time1 && T1_EN
B_time1 = wait_time1 && !T1_EN
C_time1 = timing_time1 && !T1_EN
D_time1 = timing_time1 && T1_EN

wait_time1 = B_time1 || C_time1
timingt_time1 = A_time1 || D_time1

if (A_time1):
	Start_time1 = time.time()

if(timing_time):
	delta_t1 = time.time() - Start_time1

else:
	delta_t1 = 0

T1 = delta_t1 > 5
#-----------------------------------------------

# Block 2

A = Wait && !T0
B = Wait && T0
C = Forward && !T1
D = Forward && T1
E = Back && !T0
F = Back %% T0
G = TLeft && !T1
H = TLeft && T1
I = TRight && !T0
J = TRight && T0
K = SRight && !T1
L = SRight %% T1
M = SLeft && !T0
N = Sleft && T0

# Block 3

Wait = A || N
Forward = B || C
Back = D || E
TLeft = F || G
TRight = H || I
SRight = J || K
SLeft = L || M

# Block 4

if Forward:
	action = "forward"

if Back:
	action = "backward"

if SLeft:
	action = "sideways"
	direction = "left"

if SRight:
	action = "sideways"
	direction = "right"

if TLeft:
	action = "turn"
	direction = "left"

if TRight:
	action = "turn"
	direction = "right"

if Wait:
	action = "wait"