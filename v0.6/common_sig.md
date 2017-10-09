# The Common Signals (PSS/SSS/Pilots)

All these signals PSS/SSS and Pilot tones are generated at function `[common_signal_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L513)`

* **[common_signal_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L513)**
  * [generate_pilots_slot()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pilots.c#L131)
    * [lte_dl_cell_spec()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_REFSIG/lte_dl_cell_spec.c#L280) - Insert the pilot tones into the LTE slot
  * [generate_pss()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pss.c#L42) - Generate the Primary Synchronization Signal
  * [generate_sss()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/sss.c#L39) - Generate the Secondary Synchronization Signal
  * [generate_pbch()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pbch.c#L150) 
