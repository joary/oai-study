## Downlink OFDM Modulation Process

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
