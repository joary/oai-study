
# PDCCH

From LTE specification the PDCCH carries the Downlink Control Information (DCI)

The DCI encoding have the following steps:

1. CRC Attachment
2. Channel Coding
3. Rate Maching

The encoded DCI is modulated with the following steps:

1. Multiplexing and Scrambling
2. QPSK Modulation
3. Layer Mapping
4. Precoding
5. Resource Mapping

First of all the DCI information comes from the MAC interface trhough the following function:

| Function | Doc | Src |
|--|--|--|
| get_dci_sdu() | | openair2/LAYER2/MAC/eNB_scheduler_primitives.c:98 |

Then another funtion is called to modulate the DCI information into the PDCCH:

| Function | Doc | Src |
|--|--|--|
| generate_dci_top() | Doc: | Src: openair1/PHY/LTE_TRANSPORT/dci.c:2182 |

Here there is a tree view of the generate_dci_top function and the ones called by it.

* generate_dci_top()
  * get_num_pdcch_symbols() - Evaluate the number of necessary CCE's and find the number of symbols
  * generate_pcfich() - Generate the PCFICH
    * pcfich_scrabling() - Scramle PCFICH data
    * Modulate PCFICH (SISO or TX Diversity)
    * Map into resource elements of each REG
  * generate_dci0()
    * dci_encoding()
      * ccodelte_encode() - 
      * sub_block_interleaving_cc() - 
      * lte_rate_matching_cc() - 
  * pdcch_scrambling()
  * Modulation (SISO or TX Diversity) - QPSK Modulation 
  * pdcch_interleaving()
  * Resource Element Mapping
