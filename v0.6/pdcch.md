
# PDCCH and PCFICH

From LTE specification the PDCCH carries the Downlink Control Information (DCI).
In addition to DCI there is a Control Format Indicator (CFI) wich indicates the size of PDCCH in OFDM symbols.
The CFI information is carried by the PCFICH.

## PDCCH - Encoding

First of all the DCI information comes from the MAC interface trhough the following function:

| Function | Source | Callee |
|--|--|--|
| [get_dci_sdu()](https://github.com/joary/openairinterface5g/tree/study/openair2/LAYER2/MAC/eNB_scheduler_primitives.c#L100) | openair2/LAYER2/MAC/eNB_scheduler_primitives.c:98 | openair1/SCHED/phy_procedures_lte_eNb.c:1244|

The DCI encoding and modulation have the following steps:

| # | Step | Executed at |
|--|--|--|
| 1 | CRC Attachment based on UE RNTI | [ccodelte_encode()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/ccoding_byte_lte.c#L51) |
| 2 | Channel Coding | [ccodelte_encode()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/ccoding_byte_lte.c#L51) |
| 3.1 | Rate Matching: Sub Block Interleaver |  [sub_block_interleaving_cc()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L123) |
| 3.2 | Rate Matching: Bit Collection/Selection | [lte_rate_matching_cc()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L632) |
| 4 | Multiplexing and Scrambling | pdcch_scrambling() |
| 5 | QPSK Modulation | generate_dci_top():2301 |
| 6 | Layer Mapping | [pdcch_interleaving()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dci.c#L270) |
| 7 | Precoding | generate_dci_top():2301 |
| 8 | Resource Mapping | generate_dci_top():2361 |

These steps are executed inside the following function (or one of its child)

| Function |  Source | Callee |
|--|--|--|
| generate_dci_top() | openair1/PHY/LTE_TRANSPORT/dci.c:2182 | /openair1/SCHED/phy_procedures_lte_eNb.c:1387 |

There is a tree view of the main procedures and functions executed by `generate_dci_top`

* **generate_dci_top()**
  * get_num_pdcch_symbols() - Evaluate the number of necessary CCE's and find the number of symbols
  * [generate_pcfich()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pcfich.c#L135) - Generate the PCFICH
  * [generate_dci0()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dci.c#L208)
    * [dci_encoding()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dci.c#L163)
      * [ccodelte_encode()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/ccoding_byte_lte.c#L51) - Execure Channel coding and CRC attachment
      * [sub_block_interleaving_cc()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L123) - 
      * [lte_rate_matching_cc()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/CODING/lte_rate_matching.c#L632) - 
  * pdcch_scrambling()
  * Modulation (SISO or TX Diversity) - QPSK Modulation 
  * [pdcch_interleaving()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dci.c#L270)
  * Resource Element Mapping

## PCFICH

The PCFICH is encoded together with PDCCH at the function `[generate_pcfich()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pcfich.c#L135)`

The CFI encoding and modulation have the following steps:

| # | Step | Executed at |
|--|--|--|
| 1 | Channel Coding | [pcfich_scrambling()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pcfich.c#L77) |
| 2 | Scrambling | [pcfich_scrambling()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pcfich.c#L77) |
| 3 | QPSK Modulation | [generate_pcfich()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pcfich.c#L135):164 |
| 4 | Layer Mapping |
| 5 | Precoding | [generate_pcfich()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pcfich.c#L135):164 |
| 6 | Resource Mapping | [generate_pcfich()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pcfich.c#L135):191 |

A tree view of the main procedures and functions executed at `generate_pcfich` is shown below:

* **[generate_pcfich()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/pcfich.c#L135)** - Generate the PCFICH
  * pcfich_scrabling() - Get CFI info, execute channel coding and Scramble data
  * Modulate PCFICH (SISO or TX Diversity)
  * Map into resource elements of each REG

## PDCCH - Decoding

### TODO

## PCFICH - Decoding

### TODO
