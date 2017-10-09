# PDSCH

## Downlink Shared Channel Encoding

The Downlink Shared Channel Procedures are executed at the function `[pdsch_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L938)`.

The following table shows the sequence of operations executed at the PDSCH encoding, and the respective function used to execute each step. 

| # | Procedure | Executed at | Callee |
|--|--|--|--|
| 1 | Transport Block CRC | [crc24a()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/crc_byte.c#L110) | [dlsch_encoding()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_coding.c#L560) |
| 2 | Code Block Segmentation & CRC | [lte_segmentation()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_segmentation.c#L180) | [dlsch_encoding()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_coding.c#L560) |
| 3 | Channel Coding | [threegpplte_turbo_encoder()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/3gpplte.c#L108) | [dlsch_encoding()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_coding.c#L560) |
| 4.1 | Rate Matching: Sub Block Interleaver | [sub_block_interleaving_turbo()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L45) |  [dlsch_encoding()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_coding.c#L560) |
| 4.2 | Rate Matching: Bit Collection/Selection | [lte_rate_matching_turbo()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L454) |  [dlsch_encoding()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_coding.c#L560) |
| 5 | Code Word Scrambling | dlsch_scrambling() | [pdsch_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L938) |
| 6 | Modulation Mapping | [allocate_REs_in_RB()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_modulation.c#L557) |  dlsch_modulation() |
| 7 | Layer Mapping | [allocate_REs_in_RB()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_modulation.c#L557) |  dlsch_modulation() |
| 8 | Precoding | [allocate_REs_in_RB()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_modulation.c#L557) |  dlsch_modulation() |
| 9 | Resource Mapping | [allocate_REs_in_RB()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_modulation.c#L557) | dlsch_modulation() |

Also the following tree view shows the sub-functions called by `[pdsch_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L938)`

* **[pdsch_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L938)**
  * Select wich information will be transmitted:
    * If Randon Access Response:
      * mac_xface->fill_rar()
      * [add_ue()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L146)
      * If error on [add_ue()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L146)
        * mac_xface->cancel_ra_proc()
      * [generate_eNB_ulsch_params_from_rar()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/rar_tools.c#L56)
      * mac_xface->set_msg3_subframe()
    * If Normal DLCSH data:
      * mac_xface->get_dlsch_sdu()
  * eNB->te() - Pointer to the Downlink Shared Channel Encoding Function
    * Pointer to [dlsch_encoding()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_coding.c#L560):
      * [crc24a()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/crc_byte.c#L110)
      * [lte_segmentation()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_segmentation.c#L180)
      * [threegpplte_turbo_encoder()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/3gpplte.c#L108)
      * [sub_block_interleaving_turbo()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L45)
      * [lte_rate_matching_turbo()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L454)
  * dlsch_scrambling()
  * dlsch_modulation()
    * Parse the modulation, layer-mapping and precoding parameters
    * [allocate_REs_in_RB()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_modulation.c#L557)

## Downlink Shared Channel Decoding

### TODO
