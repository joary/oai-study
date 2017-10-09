# PBCH

In the OAI implementation the PBCH is encoded together with the PSS/SSS in the function: `commong_signal_procedures:`.
This function calls the `generate_pbch` with the data to be transmitted in the broadcast channel.


## PBCH Encoding

| # | Procedure | Function |
|--|--|--|

Following a tree view of the main functions and operations called in the `generate_pbch`

* **[generate_pbch()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pbch.c#L150)**
  * [ccodelte_encode()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/ccoding_byte_lte.c#L51)
  * [sub_block_interleaving_cc()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L123)
  * [lte_rate_matching_cc()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L632)
  * [pbch_scrambling()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pbch.c#L748)
  * Modulation and Mapping
  * [allocate_pbch_REs_in_RB()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pbch.c#L55)
