
- [Important Notes:](#important-notes)
	- [Contribution:](#contribution)
- [OpenAirInterface 5G Code Study](#openairinterface-5g-code-study)
	- [The RF Frontend](#the-rf-frontend)
	- [The eNodeB Process](#the-enodeb-process)
	- [OFDM Modulation Process](#ofdm-modulation-process)

# Important Notes:

* This is a study of the PHY layer of LTE implementation of OpenAirInterface, it assumes you already know the basic LTE protocol concepts.
* This is a bottom-up perspective of the LTE eNodeB application, the simulators and emulators can be seen a sub-set of this.
* This is an interpretation of the code on [master branch](https://gitlab.eurecom.fr/oai/openairinterface5g/commit/d0e2938baabf6abf52889dec662f1abef1bc8e56), wich is still based on v0.1 of the OAI code.
* This repository does not contains any OAI code, you can find it [here](https://gitlab.eurecom.fr/oai/openairinterface5g)

## Contribution:
* The code moves fast, any error or wrong information, please contribute with merge requests.

# OpenAirInterface 5G Code Study

## The RF Frontend

Lets start at the point where the samples are sent/received to/from the RF interface. 
As a matter of fact, the OAI code can use different RF frontends (BLADERF,   ETHERNET,  EXMIMO,  LMSSDR,  USRP), which are choose at the compilation time. The code for each frontend can be found  [here](https://gitlab.eurecom.fr/oai/openairinterface5g/tree/master/targets/ARCH).

From the code perspective all these RF frontends are abstracted by a single device that contains all the functions and variables necessary to control the frontend, for example on the USRP code on the device_init() function ([here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/ARCH/USRP/USERSPACE/LIB/usrp_lib.cpp#L486)) it is possible to see the functions used to control the frontend :

```
device->trx_start_func       = trx_usrp_start;       // Starts the USRP 
device->trx_write_func       = trx_usrp_write;       // Sends samples to USRP
device->trx_read_func        = trx_usrp_read;        // Get samples from USRP
device->trx_get_stats_func   = trx_usrp_get_stats;   // Get stats of USRP
device->trx_reset_stats_func = trx_usrp_reset_stats; // Reset stats of USRP
device->trx_end_func         = trx_usrp_end;         // Finishes the communication with USRP
device->trx_stop_func        = trx_usrp_stop;        // Halts the communication with USRP
device->trx_set_freq_func    = trx_usrp_set_freq;    // Configure the USRP's channel center frequency
device->trx_set_gains_func   = trx_usrp_set_gains;   // Configure the USRP analog gains
```

It is also possible to see the same for the other frontends, just search for the device_init() function in the respective code:
* BLADERF [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/ARCH/BLADERF/USERSPACE/LIB/bladerf_lib.c#L1080)
* LMSSDR [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/ARCH/LMSSDR/USERSPACE/LIB/lms_lib.cpp#L446)
* ETHERNET [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/ARCH/ETHERNET/USERSPACE/LIB/ethernet_lib.c#L323): OBS: The Ethernet is not seen as a RF frontend but as a Fronthaul Transport frontend, although the concept changes the abstraction is the same.
* EXMIMO: The EXMIMO does not uses this abstraction, see the code [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/ARCH/EXMIMO/USERSPACE/LIB/openair0_lib.c)

Now that we now the RF frontend abstraction, let's see where these functions are called. For example the places where trx_write_func() is called are:

* eNB_transport_IQ.c [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/UE_transport_IQ.c#L390): Experimental setup for samples transport over fronthaul.
* UE_transport_IQ.c [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/eNB_transport_IQ.c#L459): Experimental setup for samples transport over fronthaul.
* lte_softmodem.c [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L2110): Main file of eNodeB application
* lte-ue.c [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-ue.c#L1345): Main file of UE application

The other functions of the RF frontend abstraction shall appear in the same files, take the exercise to find them.

## The eNodeB Process

The OpenAirInterface stack is composed of four main processes: The Evolved Packet Core, The eNodeB, The UE, and The RRH (when fronthaul is used).
Here we focus on the eNodeB process.

The main file of eNodeB application is the lte_softmodem.c this process starts six threads, the following list shows where the threads are defined and started, along with an overview of the operations executed.

* **eNB_thread**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1770), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L3750)
	* Thread to send/receive data to/from RF frontend
* **eNB_thread_tx**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1064), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1641)
	* Thread to generate the downlink signal for RF frontend
	* By default 10 threads of this function are generated.
* **eNB_thread_rx**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1367), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1642)
	* Thread to process the Uplink acquired from RF frontend
	* By default 10 threads of this function are generated.
* **scope_thread**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L550), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L3666)
	* Thread to update the information shown in the scope (enabled with -d in the command line argument)
* **emos_thread**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L719), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L3677)
	* The EMOS (Eurecom MIMO Openair Sounder) allows multi-user MIMO channel measurements in real time
	* At this commit the EMOS functions may by unstable,
	* More at [eurecon wiki](https://twiki.eurecom.fr/twiki/bin/view/OpenAirInterface/EurecomMimoOpenairSounder)
* **gps_thread**: defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L649), started [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L3679)
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
	* **phy_procedures_eNB_TX()** defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/openair1/SCHED/phy_procedures_lte_eNb.c#L517), used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1255)
	* **do_OFDM_mod_rt()** defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L947), used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1273)
* Uplink
	* **phy_procedures_eNB_RX()** defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/openair1/SCHED/phy_procedures_lte_eNb.c#L2671), used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1541)
	* **phy_procedures_eNB_S_RX()** defined [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/openair1/SCHED/phy_procedures_lte_eNb.c#L293), used [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1545)

## OFDM Modulation Process

The OFDM modulation process is based on two main functions, the following section will comment about its implementation.
* **do_OFDM_mod_rt()** [[see code](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L947)]
* **PHY_ofdm_mod()** [[see code](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/openair1/PHY/MODULATION/ofdm_mod.c#L85)]

Although the OFDM modulation is essentially simple ( Fourier Transform followed by Cyclic Prefix Insertion), there are several parameters on the LTE protocol that changes its operation, for example:

- The Duplexing Type (TDD vs FDD)
- The Subframe Allocation Configuration (which subframes are for Downlink, Uplink or Special Subframe)
- The Cyclic Prefix Size (Normal vs Extended)
- The Cyclic Prefix for symbol 0 in Normal Mode

The function **do_OFDM_mod_rt()** [[see code](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L947)] takes care of these details for the Downlink. 
On each function call a hole subframe will be processed.
As a matter of fact the do_OFDM_mod_rt() is just a wrapper to the **PHY_ofdm_mod()** which actually modulates the data into OFDM signal.

The **PHY_ofdm_mod()** [[see code](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/openair1/PHY/MODULATION/ofdm_mod.c#L85)] receives complex samples in the frequency domain, and generates complex samples in the time domain with cyclic prefix.
In addition the function can process more than one OFDM symbol, as long as the fftsize and cyclic prefix size are the same among them.

In the **do_OFDM_mod_rt()** it is possible to see the usage of **PHY_ofdm_mod()** to modulate the 12 symbols of a subframe (6 for each slot) in Extended Mode [here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L968).
In addition in order to modulate the subframe for normal mode a wrapper is created, called **norma_prefix_mod()** [[code here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/openair1/PHY/MODULATION/ofdm_mod.c#L47)], since in normal mode there is a change in the Cyclic Prefix on the First OFDM symbol of the slot.

The **do_OFDM_mod_rt()** also keeps track of which subframe is being modulated, in order to skip the frames allocated for Uplink given the TDD configuration used [[see here](https://gitlab.eurecom.fr/oai/openairinterface5g/blob/master/targets/RT/USER/lte-softmodem.c#L1026)]
