import time

# Block 1

T0_EN = Wait or Back or TRight or SLeft
T1_EN = Forward or TLeft or SRight

# --------------------TIMER_0--------------------
A_time0 = wait_time0 and T0_EN
B_time0 = wait_time0 and not T0_EN
C_time0 = timing_time0 and not T0_EN
D_time0 = timing_time0 and T0_EN

wait_time0 = B_time0 or C_time0
timingt_time0 = A_time0 or D_time0

if (A_time0):
	Start_time0 = time.time()

if(timing_time):
	delta_t0 = time.time() - Start_time0

else:
	delta_t0 = 0

T0 = delta_t0 > 5
#-----------------------------------------------

#--------------------TIMER_1--------------------
A_time1 = wait_time1 and T1_EN
B_time1 = wait_time1 and not T1_EN
C_time1 = timing_time1 and not T1_EN
D_time1 = timing_time1 and T1_EN

wait_time1 = B_time1 or C_time1
timingt_time1 = A_time1 or D_time1

if (A_time1):
	Start_time1 = time.time()

if(timing_time):
	delta_t1 = time.time() - Start_time1

else:
	delta_t1 = 0

T1 = delta_t1 > 5
#-----------------------------------------------

# Block 2

A = Wait and not T0
B = Wait and T0
C = Forward and not T1
D = Forward and T1
E = Back and not T0
F = Back and T0
G = TLeft and not T1
H = TLeft and T1
I = TRight and not T0
J = TRight and T0
K = SRight and not T1
L = SRight and T1
M = SLeft and not T0
N = Sleft and T0

# Block 3

Wait = A or N
Forward = B or C
Back = D or E
TLeft = F or G
TRight = H or I
SRight = J or K
SLeft = L or M

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