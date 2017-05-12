toc

# Important Notes:

* This is a study of the PHY laywer of LTE implementation of OpenAirInterface.
* This is a botton-up perspective of the LTE eNodeB application, the simulators and emulators can be seen a sub-set of this.
* This is an interpretation of the code on [master branch](https://gitlab.eurecom.fr/oai/openairinterface5g/commit/d0e2938baabf6abf52889dec662f1abef1bc8e56), wich is still based on v0.1 of the OAI code.
* This repository does not contains any OAI code, you can find it [here](https://gitlab.eurecom.fr/oai/openairinterface5g)

## Contribution:
* The code moves fast, any error or wrong information, please contribute.


# OpenAirInterface 5G Code Study

## The RF Frontend

Lets start at the point where the samples are sent/received to/from the RF interface. 
As a matter of fact, the OAI code can use different RF frontends (BLADERF,   ETHERNET,  EXMIMO,  LMSSDR,  USRP), which are choosed at the compilation time. The code for each frontend can be found  [here](https://gitlab.eurecom.fr/oai/openairinterface5g/tree/master/targets/ARCH).

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
