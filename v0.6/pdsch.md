# PDSCH

## Downlink Shared Channel Encoding

The Downlink Shared Channel Procedures are executed at the function `pdsch_procedures()`.

The following table shows the sequence of operations executed at the PDSCH encoding, and the respective function used to execute each step. 

| # | Procedure | Executed at | Callee |
|--|--|--|--|
| 1 | Transport Block CRC | crc24a() | dlsch_encoding() |
| 2 | Code Block Segmentation & CRC | lte_segmentation() | dlsch_encoding() |
| 3 | Channel Coding | threegpplte_turbo_encoder() | dlsch_encoding() |
| 4.1 | Rate Matching: Sub Block Interleaver | sub_block_interleaving_turbo() |  dlsch_encoding() |
| 4.2 | Rate Matching: Bit Collection/Selection | lte_rate_matching_turbo() |  dlsch_encoding() |
| 5 | Code Word Scrambling | dlsch_scrambling() | pdsch_procedures() |
| 6 | Modulation Mapping | allocate_REs_in_RB() |  dlsch_modulation() |
| 7 | Layer Mapping | allocate_REs_in_RB() |  dlsch_modulation() |
| 8 | Precoding | allocate_REs_in_RB() |  dlsch_modulation() |
| 9 | Resource Mapping | allocate_REs_in_RB() | dlsch_modulation() |

Also the following tree view shows the sub-functions called by `pdsch_procedures()`

* **pdsch_procedures()**
  * Select wich information will be transmitted:
    * If Randon Access Response:
      * mac_xface->fill_rar()
      * add_ue()
      * If error on add_ue()
        * mac_xface->cancel_ra_proc()
      * generate_eNB_ulsch_params_from_rar()
      * mac_xface->set_msg3_subframe()
    * If Normal DLCSH data:
      * mac_xface->get_dlsch_sdu()
  * eNB->te() - Pointer to the Downlink Shared Channel Encoding Function
    * Pointer to dlsch_encoding():
      * crc24a()
      * lte_segmentation()
      * threegpplte_turbo_encoder()
      * sub_block_interleaving_turbo()
      * lte_rate_matching_turbo()
  * dlsch_scrambling()
  * dlsch_modulation()
    * Parse the modulation, layer-mapping and precoding parameters
    * allocate_REs_in_RB()

## Downlink Shared Channel Decoding

### TODO
