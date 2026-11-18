--------------------------- MODULE FirewallEpochs ---------------------------
EXTENDS Naturals, Integers
CONSTANTS Mode, MaxEpoch
VARIABLES issued, ack, policy, disk, receipt, conn, alive, active, rebooted
vars == <<issued, ack, policy, disk, receipt, conn, alive, active, rebooted>>
Init == /\ issued = 0 /\ ack = 0 /\ policy = 0 /\ disk = 0
        /\ receipt = 0 /\ conn = 0 /\ alive = TRUE /\ active = FALSE
        /\ rebooted = FALSE
Issue == /\ alive /\ issued = ack /\ issued < MaxEpoch
         /\ issued' = issued + 1
         /\ UNCHANGED <<ack, policy, disk, receipt, conn, alive, active, rebooted>>
Policy(g) == /\ ((Mode = "regressive_policy" /\ g # policy) \/ g > policy)
             /\ policy' = g /\ conn' = -1
             /\ UNCHANGED <<issued, ack, disk, receipt, alive, active, rebooted>>
Persist == /\ policy > disk /\ disk' = policy
           /\ UNCHANGED <<issued, ack, policy, receipt, conn, alive, active, rebooted>>
ReceiptSource == IF Mode = "volatile_receipt" THEN policy ELSE disk
Receipt == /\ alive /\ ReceiptSource > receipt /\ receipt' = ReceiptSource
           /\ UNCHANGED <<issued, ack, policy, disk, conn, alive, active, rebooted>>
Ack == /\ alive /\ issued > ack
       /\ (Mode = "local_ack" \/ receipt >= issued)
       /\ ack' = issued
       /\ UNCHANGED <<issued, policy, disk, receipt, conn, alive, active, rebooted>>
Session(g) == /\ g % 2 = 0 /\ g # conn
              /\ (Mode = "session_bypass" \/ g = policy)
              /\ conn' = g
              /\ UNCHANGED <<issued, ack, policy, disk, receipt, alive, active, rebooted>>
Restart == /\ ~rebooted /\ policy' = disk /\ conn' = 0 /\ rebooted' = TRUE
           /\ UNCHANGED <<issued, ack, disk, receipt, alive, active>>
Crash == /\ alive /\ issued > 0 /\ alive' = FALSE
         /\ UNCHANGED <<issued, ack, policy, disk, receipt, conn, active, rebooted>>
Takeover == /\ ~alive /\ ~active /\ active' = TRUE
            /\ UNCHANGED <<issued, ack, policy, disk, receipt, conn, alive, rebooted>>
Next == Issue \/ Persist \/ Receipt \/ Ack \/ Restart \/ Crash \/ Takeover
        \/ (\E g \in 0..issued : Policy(g) \/ Session(g))
Admit == IF active THEN
           IF Mode = "session_bypass" THEN conn >= 0
           ELSE policy % 2 = 0 /\ conn = policy
         ELSE alive /\ issued % 2 = 0
Safe == ~(ack % 2 = 1 /\ issued = ack /\ Admit)
TypeOK == /\ issued \in 0..MaxEpoch /\ ack \in 0..MaxEpoch
          /\ policy \in 0..MaxEpoch /\ disk \in 0..MaxEpoch
          /\ receipt \in 0..MaxEpoch /\ conn \in {-1} \cup (0..MaxEpoch)
          /\ alive \in BOOLEAN /\ active \in BOOLEAN /\ rebooted \in BOOLEAN
ProtectedOrder == (Mode # "protected") \/ (ack <= receipt /\ receipt <= disk /\ disk <= policy /\ policy <= issued)
Spec == Init /\ [][Next]_vars
=============================================================================
