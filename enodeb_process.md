## The eNodeB Process

On this study we focus on the eNodeB process of OpenAirInterface, but there are other three main components: The Evolved Packet Core, The UE and The RRH (when fronthaul is used)

The main file of eNodeB application is the lte_softmodem.c this process starts six threads, the following list shows where these threads are defined and started, along with the purpose of each thread.

* **eNB_thread**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L1770), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L3750)
	* Thread to send/receive data to/from RF frontend
* **eNB_thread_tx**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L1064), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L1641)
	* Thread to generate the downlink signal for RF frontend
	* By default 10 threads of this type are generated.
* **eNB_thread_rx**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L1367), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L1642)
	* Thread to process the Uplink acquired from RF frontend
	* By default 10 threads of this type are generated.
* **scope_thread**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L550), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L3666)
	* Thread to update the information shown in the scope (enabled with -d in the command line argument)
* **emos_thread**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L719), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L3677)
	* The EMOS (Eurecom MIMO Openair Sounder) allows multi-user MIMO channel measurements in real time
	* At this commit the EMOS functions may by unstable,
	* More at [eurecon wiki](https://twiki.eurecom.fr/twiki/bin/view/OpenAirInterface/EurecomMimoOpenairSounder)
* **gps_thread**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L649), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L3679)
	* GPS synchronization reference used at EMOS

Since in this study we are interested in the LTE signal, just the second and third threads are focused, the following list shows an overview of the operations done in both eNB_thread_tx and eNB_thread_rx.

* **eNB_thread_tx**
	1. Configure the thread affinity if the CPU have more than 2 processors
	2. Configure Scheduling priority
	3. Infinity Loop:
		1. Block and/or wait on Mutexes
		2. Call **phy_procedures_eNB_TX()** to generate LTE data.
		3. Call **do_OFDM_mod_rt()** to modulate LTE signal.
		4. Unlock Mutexes

* **eNB_thread_rx**
	1. Configure the thread affinity if the CPU have more than 2 processors
	2. Configure Scheduling priority
	3. Infinity Loop:
		1. Block and/or wait on Mutexes
		2. If (TDD and subframe_rx == SF_UL) or (FDD):
			1. Call **phy_procedures_eNB_RX()** to generate LTE data.
		3. If subframe_rx == SF_S
			1. Call **phy_procedures_eNB_S_RX()** to demodulate LTE signal.
		4. Unlock Mutexes


**OBS:** The thread affinity configured in both threads follows the rule:
* CPU 0 is reserved for UHD threads
* CPU 1 is reserved for TX threads
* CPU 2 ... MAX_CPUS are reserved for RX threads.

From both threads we divide the functions in Downlink and Uplink as shown in the following list:

* Downlink:
	* **phy_procedures_eNB_TX()** defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L517), used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L1255)
	* **do_OFDM_mod_rt()** defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L947), used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L1273)
* Uplink
	* **phy_procedures_eNB_RX()** defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L2671), used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L1541)
	* **phy_procedures_eNB_S_RX()** defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/openair1/SCHED/phy_procedures_lte_eNb.c#L293), used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/v0.5.2/targets/RT/USER/lte-softmodem.c#L1545)
