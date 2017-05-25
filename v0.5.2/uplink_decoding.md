## Uplink Decodification

As shown in section [The EnodeB Process](#the-enodeb-process), the uplink is processed in **eNB_thread_rx** function. This function will call the **phy_procedures_eNB_RX** in order to demodulate and decode the LTE signal.
This function expects to receive the a whole subframe (12 or 14 LTE OFDM symbols)

First of all, it is mandatory to remove to remove the 7.5kHz frequency offset that the uplink signal has. This procedures is executed [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2706) by the **remove_7_5_kHz** function [[see code](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/PHY/MODULATION/ul_7_5_kHz.c#L152)], this function is a simple complex multiplication, but its implementation gets very complex due to the processor optimization.

After that, the eNB analyses, based in the frame configuration, if the current subframe should have a PRACH information, as shown [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2711).
If the PRACH exist it is decoded by the **prach_procedures** function, defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2063).
This function calls three other important functions, as listed below:

* **prach_procedures()**: used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2713), defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2063)
	* **rx_prach()**: used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2082), defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/PHY/LTE_TRANSPORT/prach.c#L1061)
		* Searchs for the PRACH preamble 
		* Calculates the DFT based on the OFDM symbol size
		* Multiply the the result by Xu (??)
		* Calculate the IDFT based on PRACH configuration
		* Create an energy list of the preambles
	* **find_next_ue_index()**: used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2126), defined [here](::aoi_code::/openair1/SCHED/phy_procedures_lte_eNb.c#L209)
		* Get the an UE based on preamble energy list
	* **initiate_ra_proc()**: used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2164), defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair2/LAYER2/MAC/eNB_scheduler_RA.c#L739)
		* Initiate one Random Acess with the found preamble index

After the PRACH search, the code demodulates the SC-FDM symbols with the function **slot_fep_ul**, as shown  [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2722).
This function will actually execute the DFT, remove the cyclic prefix, and calculate the IDFT, as shown [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/PHY/MODULATION/slot_fep_ul.c#L34).
After the SC-FDMA demodulation we are half-way from the data of ULSCH and PUCCH.

In order to process the PUCCH data, it is necessary to discober the HARQ pid based on frame and subframe info as made  [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#2742).
Then if the PUCCH is existent is can be decoded by the function **pucch_procedures**.

- pucch_procedures:
	TODO:
