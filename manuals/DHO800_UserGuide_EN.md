# DHO800 Series

## Digital Oscilloscope

**User Guide**  
Dec. 2024

## Guaranty and Declaration

### Copyright

© 2024 RIGOL TECHNOLOGIES CO., LTD. All Rights Reserved.

### Trademark Information

RIGOL® is the trademark of RIGOL TECHNOLOGIES CO., LTD.

### Notices

• RIGOL products are covered by P.R.C. and foreign patents, issued and pending.

• RIGOL reserves the right to modify or change parts of or all the specifications and pricing policies at the company's sole decision.

• Information in this publication replaces all previously released materials.

• Information in this publication is subject to change without notice.

• RIGOL shall not be liable for either incidental or consequential losses in connection with the furnishing, use, or performance of this manual, as well as any information contained.

• Any part of this document is forbidden to be copied, photocopied, or rearranged without prior written approval of RIGOL.

### Product Certification

RIGOL guarantees that this product conforms to the national and industrial standards in China as well as the ISO9001:2015 standard and the ISO14001:2015 standard. Other international standard conformance certifications are in progress.

### Contact Us

If you have any problem or requirement when using our products or this manual, please contact RIGOL.

E-mail: service@rigol.com

Website: http://www.rigol.com

## Table of Contents

| Section | Description | Page |
|---------|-------------|------|
| List of Figures | | VII |
| List of Tables | | XII |
| **1 Safety Requirement** | | **1** |
| 1.1 | General Safety Summary | 1 |
| 1.2 | Safety Notices and Symbols | 3 |
| 1.3 | Measurement Category | 3 |
| 1.4 | Ventilation Requirement | 4 |
| 1.5 | Working Environment | 4 |
| 1.6 | Care and Cleaning | 6 |
| 1.7 | Environmental Considerations | 6 |
| **2 Product Features** | | **8** |
| **3 Document Overview** | | **9** |
| **4 Quick Start** | | **11** |
| 4.1 | General Inspection | 11 |
| 4.2 | Appearance and Dimensions | 11 |
| 4.3 | To Prepare for Use | 12 |
| | 4.3.1 To Adjust the Supporting Legs | 12 |
| | 4.3.2 To Connect to Power | 13 |
| | 4.3.3 Turn-on Checkout | 13 |
| | 4.3.4 To Set the System Language | 14 |
| | 4.3.5 To Connect the Probe | 14 |
| | 4.3.6 Function Inspection | 15 |
| | 4.3.7 Probe Compensation | 16 |
| 4.4 | Product Overview | 17 |
| | 4.4.1 Front Panel Overview | 18 |
| | 4.4.2 Rear Panel Overview | 24 |
| | 4.4.3 User Interface Overview | 25 |
| 4.5 | Touch Screen Gestures | 27 |
| | 4.5.1 Tap | 28 |
| | 4.5.2 Drag | 28 |
| | 4.5.3 Pinch&Stretch | 29 |
| 4.6 | Parameter Setting Method | 30 |
| 4.7 | To Use the Security Lock | 35 |
| 4.8 | To Use the Built-in Help System | 36 |
| **5 Vertical System** | | **37** |
| 5.1 | To Enable or Disable the Analog Channel | 37 |
| 5.2 | To Adjust the Vertical Scale | 38 |
| 5.3 | To Adjust the Vertical Offset | 40 |
| 5.4 | To Specify Channel Coupling | 41 |
| 5.5 | To Specify Bandwidth Limit | 41 |
| 5.6 | To Specify Input Impedance | 42 |
| 5.7 | To Invert a Waveform | 42 |
| 5.8 | To Set Probe | 43 |
| 5.9 | To Specify the Amplitude Unit | 45 |
| 5.10 | To Adjust Bias | 45 |
| 5.11 | To Specify the Skew | 46 |
| 5.12 | To Turn the Channel Label Display On/Off | 46 |
| **6 Horizontal System** | | **48** |
| 6.1 | To Adjust the Horizontal Time Base | 48 |
| 6.2 | To Adjust the Horizontal Position | 49 |
| 6.3 | Zoom Mode (Delayed Sweep) | 50 |
| **7 Acquisition System** | | **52** |
| 7.1 | Acquisition Mode | 52 |
| 7.2 | Sampling Mode | 54 |
| 7.3 | Sample Rate | 55 |
| 7.4 | Memory Depth | 56 |
| 7.5 | Horizontal Expansion Reference | 57 |
| 7.6 | Roll Mode | 58 |
| 7.7 | XY Mode | 58 |
| **8 Triggering the Oscilloscope** | | **62** |
| 8.1 | Trigger Source | 62 |
| 8.2 | Trigger Level | 63 |
| 8.3 | Trigger Mode | 63 |
| 8.4 | Trigger Coupling | 65 |
| 8.5 | Trigger Holdoff | 65 |
| 8.6 | Noise Rejection | 66 |
| 8.7 | Trigger Type | 66 |
| | 8.7.1 Edge Trigger | 67 |
| | 8.7.2 Pulse Width Trigger | 68 |
| | 8.7.3 Slope Trigger | 71 |
| Section | Description | Page |
|---------|-------------|------|
| | 8.7.4 Video Trigger | 74 |
| | 8.7.5 Pattern Trigger | 76 |
| | 8.7.6 Duration Trigger | 79 |
| | 8.7.7 Timeout Trigger | 82 |
| | 8.7.8 Runt Trigger | 84 |
| | 8.7.9 Window Trigger | 86 |
| | 8.7.10 Delay Trigger | 88 |
| | 8.7.11 Setup/Hold Trigger | 91 |
| | 8.7.12 Nth Edge Trigger | 93 |
| | 8.7.13 RS232 Trigger | 96 |
| | 8.7.14 I2C Trigger | 98 |
| | 8.7.15 SPI Trigger | 102 |
| | 8.7.16 CAN Trigger | 105 |
| 8.8 | Trigger Output Connector | 108 |
| **9 Math Operation** | | **110** |
| 9.1 | Arithmetic Operation | 111 |
| 9.2 | Function Operation | 114 |
| 9.3 | FFT Operation | 118 |
| 9.4 | Logic Operation | 123 |
| 9.5 | Digital Filter | 126 |
| **10 Measurements** | | **131** |
| 10.1 | Auto Scale | 131 |
| 10.2 | Auto Measurements | 132 |
| | 10.2.1 Measurement Parameter | 132 |
| | 10.2.1.1 Time Parameters | 132 |
| | 10.2.1.2 Count Values | 133 |
| | 10.2.1.3 Delay and Phase Parameters | 135 |
| | 10.2.1.4 Voltage Parameters | 137 |
| | 10.2.1.5 Other Parameters | 138 |
| | 10.2.2 Select the Measurement Item | 139 |
| | 10.2.3 Measurement Settings | 141 |
| | 10.2.4 Remove the Measurement Results | 144 |
| 10.3 | Cursor Measurements | 145 |
| | 10.3.1 Manual Mode | 147 |
| | 10.3.2 Track Mode | 149 |
| | 10.3.3 XY Mode | 152 |
| **11 Digital Voltmeter (DVM) and Frequency Counter** | | **154** |
| Section | Description | Page |
|---------|-------------|------|
| 11.1 | Digital Voltmeter (DVM) | 154 |
| | 11.1.1 Measurement Settings | 154 |
| | 11.1.2 Remove the Measurement | 156 |
| 11.2 | Frequency Counter | 156 |
| | 11.2.1 Measurement Settings | 157 |
| | 11.2.2 Reset Statistics | 158 |
| | 11.2.3 Remove the Measurement | 158 |
| **12 Histogram Analysis** | | **159** |
| 12.1 | To Enable or Disable the Histogram Function | 159 |
| 12.2 | To Select the Histogram Type | 160 |
| 12.3 | To Select the Histogram Source | 160 |
| 12.4 | To Set the Histogram Height | 160 |
| 12.5 | To Set the Histogram Range | 161 |
| 12.6 | Histogram Analysis Results | 161 |
| 12.7 | To Remove Results | 163 |
| 12.8 | To Clear Statistics | 163 |
| **13 Reference Waveform** | | **164** |
| 13.1 | To Enable Ref Function | 164 |
| 13.2 | To Set the Reference Waveform | 164 |
| 13.3 | To Set the Ref Waveform Display | 165 |
| 13.4 | Export and Import Operation | 166 |
| **14 Pass/Fail Test** | | **168** |
| 14.1 | To Enable or Disable the Pass/Fail Test Function | 169 |
| 14.2 | To Select the Source | 169 |
| 14.3 | To Create a Mask | 169 |
| 14.4 | To Set the Output Form of the Test Results | 170 |
| 14.5 | To Start or Stop the Pass/Fail Test Operation | 171 |
| 14.6 | To Display the Statistics of the Test Results | 171 |
| **15 Protocol Decoding** | | **173** |
| 15.1 | Parallel Decoding | 173 |
| | 15.1.1 Clock Setting (CLK) | 174 |
| | 15.1.2 Bus Setting | 175 |
| | 15.1.3 Display-related Settings | 176 |
| | 15.1.4 Event Table | 176 |
| 15.2 | RS232 Decoding | 177 |
| | 15.2.1 Source Setting | 179 |
| | 15.2.2 To Set Data Package | 180 |
| Section | Description | Page |
|---------|-------------|------|
| | 15.2.3 Display-related Settings | 180 |
| | 15.2.4 Event Table | 181 |
| 15.3 | I2C Decoding | 182 |
| | 15.3.1 Source Setting | 183 |
| | 15.3.2 Display-related Settings | 183 |
| | 15.3.3 Event Table | 184 |
| 15.4 | SPI Decoding | 185 |
| | 15.4.1 To Set the Source | 186 |
| | 15.4.2 To Set Mode and Data | 187 |
| | 15.4.3 Display-related Settings | 188 |
| | 15.4.4 Event Table | 188 |
| 15.5 | CAN Decoding | 189 |
| | 15.5.1 Signal Configuration | 190 |
| | 15.5.2 Display-related Settings | 191 |
| | 15.5.3 Event Table | 192 |
| **16 Multi-pane Windowing** | | **194** |
| **17 Waveform Recording and Playing** | | **196** |
| 17.1 | Common Settings | 196 |
| 17.2 | Record Options | 197 |
| 17.3 | Play Options | 198 |
| **18 Search and Navigation** | | **201** |
| 18.1 | Search | 201 |
| 18.2 | Navigation | 203 |
| **19 Display Control** | | **207** |
| 19.1 | Display Type | 207 |
| 19.2 | Persistence Time | 207 |
| 19.3 | Waveform Intensity | 208 |
| 19.4 | To Set the Screen Grid | 208 |
| 19.5 | Display Settings | 208 |
| 19.6 | Show Scale | 209 |
| 19.7 | Color Grade | 209 |
| 19.8 | Waveform Freeze | 209 |
| **20 Store and Load** | | **210** |
| 20.1 | To Enter the Storage Menu | 210 |
| 20.2 | To Save a File | 210 |
| | 20.2.1 To Save Image | 210 |
| | 20.2.2 To Save Wave | 212 |
| Section | Description | Page |
|---------|-------------|------|
| | 20.2.3 To Save Setup | 214 |
| | 20.2.4 Binary Data Format (.bin) | 215 |
| 20.3 | To Load a File | 218 |
| 20.4 | Firmware Upgrade | 219 |
| 20.5 | Disk Management | 220 |
| 20.6 | SMB Configuration | 222 |
| **21 System Utility Function Setting** | | **227** |
| 21.1 | I/O Setting | 227 |
| 21.2 | Basic Settings | 229 |
| 21.3 | About this Oscilloscope | 231 |
| 21.4 | Other Settings | 232 |
| 21.5 | Auto Config | 232 |
| 21.6 | SelfCal | 233 |
| 21.7 | Option List | 233 |
| 21.8 | Quick Action Settings | 233 |
| 21.9 | Self-check | 236 |
| **22 Remote Control** | | **237** |
| 22.1 | Remote Control via USB | 238 |
| 22.2 | Remote Control via LAN | 238 |
| **23 Troubleshooting** | | **240** |
| **24 Appendix** | | **241** |
| 24.1 | Appendix A: Options and Accessories | 241 |
| 24.2 | Appendix B: Warranty | 241 |
| 24.3 | Appendix C: Factory Settings | 242 |
## List of Figures

Figure 4.1 Front View .............................................................................................................11
Figure 4.2 Side View ................................................................................................................12
Figure 4.3 Adjusting the Supporting Legs ......................................................................12
Figure 4.4 To Connect to Power ..........................................................................................13
Figure 4.5 Connecting the Passive Probe ........................................................................15
Figure 4.6 Using the Compensation Signal ....................................................................16
Figure 4.7 Square Waveform Signal ..................................................................................16
Figure 4.8 Probe Compensation .........................................................................................17
Figure 4.9 Front Panel (2-channel Model) .......................................................................18
Figure 4.10 Front Panel (4-channel Model) ....................................................................18
Figure 4.11 Rear Panel ............................................................................................................24
Figure 4.12 User Interface .....................................................................................................25
Figure 4.13 Tap Gesture .........................................................................................................28
Figure 4.14 Drag Gesture ......................................................................................................29
Figure 4.15 Pinch&Stretch Gesture ....................................................................................29
Figure 4.16 English Input Interface ....................................................................................30
Figure 4.17 Chinese Input Interface ...................................................................................32
Figure 4.18 String Keypad .....................................................................................................33
Figure 4.19 Numeric Keypad ................................................................................................34
Figure 4.20 To Use the Security Lock ................................................................................35
Figure 5.1 Vertical Menu .......................................................................................................37
Figure 5.2 Waveform Invert On/Off ..................................................................................43
Figure 5.3 Probe Setting Menu ...........................................................................................43
Figure 5.4 Zero Offset ............................................................................................................46
Figure 6.1 Horizontal Menu .................................................................................................48
Figure 6.2 Zoom Mode ..........................................................................................................51
Figure 7.1 Horizontal Menu .................................................................................................52
Figure 7.2 Display Modes ......................................................................................................54
Figure 7.3 Memory Depth ....................................................................................................56
Figure 7.4 XY Menu .................................................................................................................59
Figure 7.5 Measurement Schematic Diagram of Phase Deviation .........................60
Figure 8.1 Schematic Diagram of the Acquisition Memory ......................................64
Figure 8.2 Trigger Holdoff .....................................................................................................66
Figure 8.3 Edge Trigger Setting Menu ..............................................................................67
Figure 8.4 Positive/Negative Pulse Width .......................................................................69
Figure 8.5 Pulse Width Trigger Setting Menu ................................................................69
Figure 8.6 Positive Slope Time/Negative Slope Time .................................................71
Figure 8.7 Slope Trigger Setting Menu .............................................................................72
Figure 8.8 Video Trigger Setting Menu ............................................................................74
Figure 8.9 Pattern Trigger .....................................................................................................77
Figure 8.10 Pattern Trigger Setting Menu .......................................................................77
Figure 8.11 Duration Trigger ................................................................................................79
Figure 8.12 Duration Trigger Setting Menu ....................................................................80
Figure 8.13 Timeout Trigger .................................................................................................82
Figure 8.14 Timeout Trigger Menu ....................................................................................82
Figure 8.15 Runt Trigger ........................................................................................................84
Figure 8.16 Runt Trigger Setting Menu ............................................................................84
Figure 8.17 Window Trigger Setting Menu .....................................................................86
Figure 8.18 Delay Trigger ......................................................................................................88
Figure 8.19 Delay Trigger Setting Menu ..........................................................................89
Figure 8.20 Setup/Hold Trigger ...........................................................................................91
Figure 8.21 Setup/Hold Trigger Setting Menu ...............................................................92
Figure 8.22 Nth Edge Trigger ...............................................................................................94
Figure 8.23 Nth Edge Trigger Setting Menu ...................................................................94
Figure 8.24 Schematic Diagram of RS232 Protocol .....................................................96
Figure 8.25 RS232 Trigger Setting Menu .........................................................................96
Figure 8.26 Sequence Diagram of I2C Protocol ............................................................99
Figure 8.27 I2C Trigger Setting Menu ...............................................................................99
Figure 8.28 Binary Format Setting ...................................................................................101
Figure 8.29 Hexadecimal Format Setting ......................................................................101
Figure 8.30 Sequential Chart of SPI Bus ........................................................................102
Figure 8.31 SPI Trigger Setting Menu ............................................................................ 103
Figure 8.32 Data Frame Format of the CAN Bus ........................................................105
Figure 8.33 CAN Trigger Setting Menu ..........................................................................106
Figure 8.34 Sample Position ..............................................................................................107
Figure 9.1 Math Menu .........................................................................................................110
Figure 9.2 Waveform Display Window of the Operation Results .........................111
Figure 9.3 Arithmetic Operation Menu ..........................................................................112
Figure 9.4 Operation Result Display Window ..............................................................112
Figure 9.5 Function Operation Menu .............................................................................115
Figure 9.6 Operation Result Display Window ..............................................................116
Figure 9.7 FFT Operation Menu ....................................................................................... 119
Figure 9.8 FFT Operation Window .................................................................................. 119
Figure 9.9 Peak Search .........................................................................................................122
Figure 9.10 Logic Operation Menu ................................................................................. 123
Figure 9.11 Operation Result Display Window ...........................................................125
Figure 9.12 Digital Filter Menu .........................................................................................127
Figure 9.13 Operation Result Display Window ...........................................................128
Figure 10.1 Time Parameters .............................................................................................132
Figure 10.2 Delay and Phase Parameters ......................................................................135
Figure 10.3 Voltage Parameters ....................................................................................... 137
Figure 10.4 Vertical Measurement Items ...................................................................... 139
Figure 10.5 Horizontal Measurement Items ................................................................ 140
Figure 10.6 Other Measurement Items ..........................................................................140
Figure 10.7 Measurement Settings Menu .................................................................... 141
Figure 10.8 Cursors ...............................................................................................................145
Figure 10.9 Manual Mode Setting Menu ......................................................................147
Figure 10.10 Manual Cursor Measurement Example ................................................149
Figure 10.11 Track Mode Setting Menu ........................................................................150
Figure 10.12 Track Measurement (before Horizontal Expansion) ........................151
Figure 10.13 Track Measurement (after Horizontal Expansion) ............................152
Figure 10.14 XY Mode Setting Menu ............................................................................152
Figure 11.1 DVM Setting Menu ........................................................................................155
Figure 11.2 Frequency Counter Setting Menu ............................................................157
Figure 12.1 Histogram Menu ............................................................................................159
Figure 12.2 Histogram Analysis Interface .....................................................................160
Figure 12.3 Histogram Analysis Results .........................................................................162
Figure 13.1 Reference Waveform Menu ........................................................................164
Figure 14.1 PassFail Menu ..................................................................................................168
Figure 14.2 PassFail Menu-Simplified ............................................................................168
Figure 14.3 Pass/Fail Test Interface .................................................................................171
Figure 15.1 Schematic Diagram of Parallel Decoding ..............................................173
Figure 15.2 Parallel Decoding Menu ..............................................................................174
Figure 15.3 Parallel Decoding Event Table ....................................................................177
Figure 15.4 Schematic Diagram of RS232 Serial Bus ................................................178
Figure 15.5 RS232 Decoding Menu ................................................................................178
Figure 15.6 RS232 Decoding Event Table .....................................................................181
Figure 15.7 I2C Serial Bus ...................................................................................................182
Figure 15.8 I2C Decoding Menu ......................................................................................182
Figure 15.9 I2C Decoding Event Table ...........................................................................184
Figure 15.10 SPI Serial Bus .................................................................................................185
Figure 15.11 SPI Decoding Menu ....................................................................................186
Figure 15.12 SPI Decoding Event Table .........................................................................189
Figure 15.13 CAN Decoding Menu .................................................................................190
Figure 15.14 Sample Position ............................................................................................191
Figure 15.15 CAN Decoding Event Table ...................................................................... 192
Figure 16.1 "Add Window" Menu ....................................................................................194
Figure 17.1 "Record" Menu ................................................................................................196
Figure 17.2 Minimized "Play" Menu ............................................................................... 199
Figure 18.1 Search Menu ....................................................................................................201
Figure 18.2 MarkTable Display ..........................................................................................203
Figure 18.3 Navigation Menu ........................................................................................... 204
Figure 18.4 Simplified Navigation Menu ...................................................................... 204
Figure 18.5 "Search Event" Navigation Setting Menu ..............................................205
Figure 18.6 "Frame Segment" Navigation Setting Menu ........................................205
Figure 19.1 Display Setting Menu ................................................................................... 207
Figure 20.1 Image Saving Setting Menu .......................................................................211
Figure 20.2 Waveform Saving Setting Menu ...............................................................213
Figure 20.3 Setup Saving Setting Menu ........................................................................214
Figure 20.4 Load Setting Menu ........................................................................................219
Figure 20.5 Upgrade Menu ................................................................................................220
Figure 20.6 Disk Management Interface .......................................................................221
Figure 20.7 SMB Setting Menu .........................................................................................223
Figure 21.1 Self-calibration Menu ................................................................................... 233
Figure 21.2 Quick Menu ......................................................................................................234
## List of Tables

Table 4.1 Power Adaptor Specifications ...........................................................................13

Table 5.1 Probe Ratio ..............................................................................................................44

Table 8.1 Video Standard ...................................................................................................... 75

Table 9.1 Window Function ................................................................................................121

Table 9.2 Logic Operation .................................................................................................. 124

Table 15.1 Bus Setting ..........................................................................................................175

Table 20.1 BIN File Format ................................................................................................. 215

Table 20.2 File Header ..........................................................................................................216

Table 20.3 Waveform Header ............................................................................................216

Table 20.4 Waveform Data Header ................................................................................. 218

Table 24.2 Factory Settings ................................................................................................242

# 1 Safety Requirement

## 1.1 General Safety Summary

Please review the following safety precautions carefully before putting the instrument into operation so as to avoid any personal injury or damage to the instrument and any product connected to it. To prevent potential hazards, please follow the instructions specified in this manual to use the instrument properly.

• **Use Proper Power Cord.**

Only the exclusive power cord designed for the instrument and authorized for use within the destination country could be used.

• **Ground the Product Properly.**

The instrument uses the Type-C power interface. The instrument is not grounded via the power cord. To avoid electric shock, use the ground cable provided in accessories to connect the instrument to the earth ground before connecting any input or output terminals.

• **Make Measurements Properly.**

This product is a non-isolated oscilloscope. The ground (GND) for each input and output interface is not isolated from the metal chassis or the digital interface grounds (such as USB and HDMI). Do not perform floating measurements without using isolated probes, nor connect any port's GND to a port with a voltage difference relative to earth ground. Otherwise, it may cause damage to this product or other devices (such as the DUT or a computer display) connected to the product and can even cause serious personal injury.

• **Connect the Probe Properly.**

If a probe is used, the probe ground lead must be connected to earth ground. Do not connect the ground lead to high voltage. Improper way of connection could result in dangerous voltages being present on the connectors, controls or other surfaces of the oscilloscope and probes, which will cause potential hazards for operators.

• **Observe All Terminal Ratings.**

To avoid fire or shock hazard, observe all ratings and markers on the instrument and check your manual for more information about ratings before connecting the instrument.

• **Use Proper Overvoltage Protection.**

Ensure that no overvoltage (such as that caused by a bolt of lightning) can reach the product. Otherwise, the operator might be exposed to the danger of an electric shock.
• **Do Not Operate Without Covers.**

Do not operate the instrument with covers or panels removed.

• **Do Not Insert Objects into the Air Outlet.**

Do not insert objects into the air outlet, as doing so may cause damage to the instrument.

• **Avoid Circuit or Wire Exposure.**

Do not touch exposed junctions and components when the instrument is powered on.

• **Do Not Operate With Suspected Failures.**

If you suspect that any damage may occur to the instrument, have it inspected by RIGOL authorized personnel before further operations. Any maintenance, adjustment or replacement especially to circuits or accessories must be performed by RIGOL authorized personnel.

• **Provide Adequate Ventilation.**

Inadequate ventilation may cause an increase of temperature in the instrument, which would cause damage to the instrument. So please keep the instrument well ventilated and inspect the air outlet and the fan regularly.

• **Do Not Operate in Wet Conditions.**

To avoid short circuit inside the instrument or electric shock, never operate the instrument in a humid environment.

• **Do Not Operate in an Explosive Atmosphere.**

To avoid personal injuries or damage to the instrument, never operate the instrument in an explosive atmosphere.

• **Keep Instrument Surfaces Clean and Dry.**

To avoid dust or moisture from affecting the performance of the instrument, keep the surfaces of the instrument clean and dry.

• **Prevent Electrostatic Impact.**

Operate the instrument in an electrostatic discharge protective environment to avoid damage induced by static discharges. Always ground both the internal and external conductors of cables to release static before making connections.

• **Use the Battery Properly.**

Do not expose the battery (if available) to high temperature or fire. Keep it out of the reach of children. Improper change of a battery (lithium battery) may cause an explosion. Use the RIGOL specified battery only.

• **Handle with Caution.**

Please handle with care during transportation to avoid damage to keys, knobs, interfaces, and other parts on the panels.

**WARNING**

Equipment meeting Class A requirements may not offer adequate protection to broadcast services within residential environment.

## 1.2 Safety Notices and Symbols

**Safety Notices in this Manual:**

**WARNING**

Indicates a potentially hazardous situation or practice which, if not avoided, will result in serious injury or death.

**CAUTION**

Indicates a potentially hazardous situation or practice which, if not avoided, could result in damage to the product or loss of important data.

**Safety Notices on the Product:**

• **DANGER**
  It calls attention to an operation, if not correctly performed, could result in injury or hazard immediately.

• **WARNING**
  It calls attention to an operation, if not correctly performed, could result in potential injury or hazard.

• **CAUTION**
  It calls attention to an operation, if not correctly performed, could result in damage to the product or other devices connected to the product.

**Safety Symbols on the Product:**

| Hazardous Voltage | Safety Warning | Protective Earth Terminal | Chassis Ground | Test Ground |
|-------------------|----------------|---------------------------|----------------|-------------|

## 1.3 Measurement Category

**Measurement Category**

This instrument can make measurements in Measurement Category I.

**WARNING**

This instrument can only be used for measurements within its specified measurement categories.

**Measurement Category Definitions**

• Measurement category I is for measurements performed on circuits not directly connected to MAINS. Examples are measurements on circuits not derived from MAINS, and specially protected (internal) MAINS derived circuits. In the latter case, transient stresses are variable. Thus, you must know the transient withstand capability of the equipment.

• Measurement category II is for measurements performed on circuits directly connected to low voltage installation. Examples are measurements on household appliances, portable tools and similar equipment.

• Measurement category III is for measurements performed in the building installation. Examples are measurements on distribution boards, circuit-breakers, wiring (including cables, bus-bars, junction boxes, switches and socket-outlets) in the fixed installation, and equipment for industrial use and some other equipment. For example, stationary motors with permanent connection to a fixed installation.

• Measurement category IV is for measurements performed at the source of a low-voltage installation. Examples are electricity meters and measurements on primary overcurrent protection devices and ripple control units.

## 1.4 Ventilation Requirement

This instrument uses a fan to force cooling. Please make sure that the air inlet and outlet areas are free from obstructions and have free air. When using the instrument in a bench-top or rack setting, provide at least 10 cm clearance beside, above and behind the instrument for adequate ventilation.

**CAUTION**

Inadequate ventilation may cause an increase of temperature in the instrument, which would cause damage to the instrument. So please keep the instrument well ventilated and inspect the air outlet and the fan regularly.

## 1.5 Working Environment

**Temperature**

Operating: 0℃ to +50℃
Non-operating: -30℃ to +60℃

**Humidity**

• **Operating:**
  Below +30℃: ≤90%RH (without condensation)
  +30℃ to +40℃: ≤75% RH (without condensation)
  +40℃ to +50℃: ≤45%RH (without condensation)

• **Non-operating:**
  Below +60℃: ≤90%RH (without condensation)

**WARNING**

To avoid short circuit inside the instrument or electric shock, never operate the instrument in a humid environment.

**Altitude**

• Operating: below 3 km
• Non-operating: below 15 km

**Protection Level Against Electric Shock**

ESD ±8kV

**Installation (Overvoltage) Category**

This product is powered by mains conforming to installation (overvoltage) category II.

**WARNING**

Ensure that no overvoltage (such as that caused by a bolt of lightning) can reach the product. Otherwise, the operator might be exposed to the danger of an electric shock.

**Installation (Overvoltage) Category Definitions**

Installation (overvoltage) category I refers to signal level which is applicable to equipment measurement terminals connected to the source circuit. Among these terminals, precautions are done to limit the transient voltage to a low level.

Installation (overvoltage) category II refers to the local power distribution level which is applicable to equipment connected to the AC line (AC power).

**Pollution Degree**

Pollution Degree 2

**Pollution Degree Definition**

• **Pollution Degree 1:** No pollution or only dry, nonconductive pollution occurs. The pollution has no effect. For example, a clean room or air-conditioned office environment.
• **Pollution Degree 2:** Normally only nonconductive pollution occurs. Temporary conductivity caused by condensation is to be expected. For example, indoor environment.

• **Pollution Degree 3:** Conductive pollution or dry nonconductive pollution that becomes conductive due to condensation occurs. To be found in industrial environment or construction sites (harsh environments). For example, sheltered outdoor environment.

• **Pollution Degree 4:** The pollution generates persistent conductivity caused by conductive dust, rain, or snow. For example, outdoor areas.

**Safety Class**

Class 2

## 1.6 Care and Cleaning

**Care**

Do not store or leave the instrument where it may be exposed to direct sunlight for long periods of time.

**Cleaning**

Clean the instrument regularly according to its operating conditions.

1. Disconnect the instrument from all power sources.

2. Clean the external surfaces of the instrument with a soft cloth dampened with mild detergent or water. Avoid having any water or other objects into the chassis via the heat dissipation hole. When cleaning the LCD, take care to avoid scarifying it.

**CAUTION**

To avoid damage to the instrument, do not expose it to caustic liquids.

**WARNING**

To avoid short-circuit resulting from moisture or personal injuries, ensure that the instrument is completely dry before connecting it to the power supply.

## 1.7 Environmental Considerations

The following symbol indicates that this product complies with the WEEE Directive 2012/19/EU.
The equipment may contain substances that could be harmful to the environment or human health. To avoid the release of such substances into the environment and avoid harm to human health, we recommend you to recycle this product appropriately to ensure that most materials are reused or recycled properly. Please contact your local authorities for disposal or recycling information.

You can click on the following link https://int.rigol.com/services/services/declaration to download the latest version of the RoHS&WEEE certification file.

# 2 Product Features

• Ultra-low noise floor, purer signal, never miss the small signals
• Up to 12 bits resolution for all the models of this series
• Max. analog bandwidth of 100 MHz, 4 analog channels, external trigger output (std.) available for the dual-channel model
• Max. real-time sample rate of 1.25 GSa/s
• Max. memory depth of 25 Mpts
• Vertical sensitivity range: 500 μV/div to 10 V/div
• Max. capture rate of 1,000,000 wfms/s (in UltraAcquire mode)
• Digital phosphor display with real-time 256-level intensity grading
• Waveform search and navigation function allows you to debug the signal anomalies faster
• 7" (1024x600) capacitive multi-touch screen
• Brand new Flex Knob brings user-friendly experience
• USB Device & Host, LAN, and HDMI interfaces (std.) for all the models of this series
• Novel and delicate industrial design, easy to operate
• Unique online upgrade

The DHO800 series is RIGOL's new launched high-performance economical digital oscilloscope. Though compact in design, it has superior performance. It features a capture rate up to 1,000,000 wfms/s (in UltraAcquire Mode), 25 Mpts memory depth, 12 bit resolution, and low noise.

The DHO800 series is a brand new economical digital oscilloscope designed for the vast mainstream digital oscilloscope market to meet their design, debugging, and test demands.

# 3 Document Overview

This manual gives you a quick overview of the front and rear panel, user interface as well as basic operation methods of DHO800 series.

**TIP**

For the latest version of this manual, download it from RIGOL official website (http://www.rigol.com).

**Publication Number**

UGA36105-1110

**Software Version**

00.01.03

Software upgrade might change or add product features. Please acquire the latest version of the manual from RIGOL website or contact RIGOL to upgrade the software.

**Format Conventions in this Manual**

1. **Key**

The front panel key is denoted by the menu key icon. For example, **DEFAULT** indicates the "Default" key.

2. **Menu**

The menu item is denoted by the format of "Menu Name (Bold) + Character Shading" in the manual. For example, **Setup** indicates the "Setup" sub-menu under the "Utility" function menu. You can click or tap **Setup** to access the "Setup" menu.

3. **Operation Procedures**

The next step of the operation is denoted by ">" in the manual. For example, **Utility** > **Storage** indicates first clicking or tapping **Utility** and then clicking or tapping **Storage**.

4. **Connector**

The front/rear panel connector is denoted by "Brackets + Connector Name (Bold)", for example, **[AUX OUT]**.

5. **Knob**

| Label | Knob | Label | Knob |
|-------|------|-------|------|
| Horizontal **POSITION** | Horizontal Position Knob | **1** | Multipurpose Knob 1 |
| Horizontal **SCALE** | Horizontal Scale Knob | **2** | Multipurpose Knob 2 |
| Vertical **POSITION** | Vertical Position Knob | **LEVEL** | Trigger Level Knob |
| Vertical **SCALE** | Vertical Scale Knob | - | - |

**Content Conventions in this Manual**

DHO800 series digital oscilloscope includes the following models. Four-channel models and two-channel models share the same operation method. Unless otherwise specified, this manual takes the four-channel model DHO814 as an example to illustrate the operation methods of DHO800 series oscilloscope.

| Model | Max. Analog Bandwidth | No. of Analog Channels |
|-------|----------------------|------------------------|
| DHO802 | 70 MHz | 2+EXT |
| DHO804 | 70 MHz | 4 |
| DHO812 | 100 MHz | 2+EXT |
| DHO814 | 100 MHz | 4 |

# 4 Quick Start

## 4.1 General Inspection

1. **Inspect the packaging**

If the packaging has been damaged, do not dispose the damaged packaging or cushioning materials until the shipment has been checked for completeness and has passed both electrical and mechanical tests.

The consigner or carrier shall be liable for the damage to the instrument resulting from shipment. RIGOL would not be responsible for free maintenance/rework or replacement of the instrument.

2. **Inspect the instrument**

In case of any mechanical damage, missing parts, or failure in passing the electrical and mechanical tests, contact your RIGOL sales representative.

3. **Check the accessories**

Please check the accessories according to the packing lists. If the accessories are damaged or incomplete, please contact your RIGOL sales representative.

**Recommended Calibration Interval**

RIGOL suggests that the instrument should be calibrated every 18 months.

## 4.2 Appearance and Dimensions

265.36 mm × 161.75 mm
77.38 mm

Figure 4.2 Side View

## 4.3 To Prepare for Use

### 4.3.1 To Adjust the Supporting Legs

Adjust the supporting legs properly to use them as stands to tilt the oscilloscope upwards for stable placement of the oscilloscope as well as better operation and observation. You can also fold the supporting legs when the instrument is not in use for easier storage or shipment, as shown in the figure below.

Supporting Legs

(a) Unfold the supporting legs    (b) Fold the supporting legs

Figure 4.3 Adjusting the Supporting Legs

### 4.3.2 To Connect to Power

The power requirements of the oscilloscope are DC, 15 V, 3 A. Please use the power adaptor provided in the accessories to connect the oscilloscope to the AC power source (100 V to 240 V, 50 Hz to 60 Hz), as shown in the figure below.

Power Cord Connector

Figure 4.4 To Connect to Power

Table 4.1 Power Adaptor Specifications

| Item | Description |
|------|-------------|
| Input | 100 V to 240 V, 50 Hz to 60 Hz, 1.2 A Max |
| Output | DC, 15 V, 3 A, 45 W |

**CAUTION**

The power adaptor provided in accessories can only be used to power RIGOL instruments. Do not use it for mobile phone and other devices.

**WARNING**

To avoid electric shock, use the ground cable provided in the accessories to ground the instrument properly.

### 4.3.3 Turn-on Checkout

After the instrument is connected to the power source, press the power key at the lower-left corner of the front panel to power on the instrument. During the start-up
process, the instrument performs a series of self-tests. After the self-test, the splash screen is displayed.

• **Restart**: Click or tap > **Power** > **Restart** to restart the instrument.

• **Shutdown**:
  - Click or tap > **Power** > **Shutdown** to shut down the instrument.
  - Press and then click or tap **Shutdown** in the displayed "Power" menu to shut down the instrument.
  - Press twice to shut down the instrument.
  - Press for three seconds to shut down the instrument.

• **Sleep**: Click or tap > **Power** > **Sleep** to enter sleep mode. In sleep mode, not all processes are closed, resulting in slightly higher power consumption compared to shutdown mode. However, the instrument can start up more quickly and resume its previous state before sleep. When in sleep mode, press to start the instrument.

**TIP**

You can also click or tap > **Utility** > **Setup** and set the "Power status" to "Switch On". The instrument powers on once connected to power.

### 4.3.4 To Set the System Language

This oscilloscope supports multiple languages. You can click or tap > **Utility** > **Setup** > **Language** to select the system language.

### 4.3.5 To Connect the Probe

RIGOL provides passive probes for DHO800 series. For specific probe models, refer to DHO800 Data Sheet. For detailed technical information of the probes, please refer to the corresponding Probe User Guide.

**Connect the Passive Probe**

1. Connect the BNC terminal of the probe to an analog channel input terminal of the oscilloscope on the front panel as shown in the figure below.

2. Connect the ground alligator clip or spring of the probe to the circuit ground terminal, and then connect the probe tip to the circuit point to be tested.

Figure 4.5 Connecting the Passive Probe

After you connect the passive probe, check the probe function and probe compensation adjustment before making measurements. For details, please refer to Function Inspection and Probe Compensation.

### 4.3.6 Function Inspection

1. Press the front-panel **DEFAULT** and a prompt message "Restore default settings?" is displayed. Click or tap OK to restore the instrument to its factory default settings.

2. Connect the ground alligator clip of the probe to the "Ground Terminal" as shown in Figure 4.6.

3. Use the probe to connect the input terminal of CH1 and the "Compensation Signal Output Terminal" of the probe, as shown in Figure 4.6.

Compensation Signal Output Terminal Ground Terminal

Figure 4.6 Using the Compensation Signal

4. Set the probe ratio based on the attenuation of the probe, and then click or tap > Auto.

5. Observe the waveform on the display. In normal condition, you should see a square waveform similar to the waveform shown in the figure below.

Figure 4.7 Square Waveform Signal

6. Test the other channels in the same way. If you see the waveform, but the square wave is not shaped correctly as shown above, perform the procedure described in Probe Compensation. If you do not see the waveform, perform those steps again.

**WARNING**

To avoid electric shock when using the probe, please make sure that the insulated wire of the probe is in good condition. Do not touch the metallic part of the probe when the probe is connected to high voltage source.

### 4.3.7 Probe Compensation

When used for the first time, the oscilloscope probe must be compensated to match the input characteristics of the oscilloscope channel to which it is connected.
non-compensated or poorly compensated probe may cause measurement errors. The compensation procedure is as follows:

1. Perform Step 1, 2, 3 and 4 in Function Inspection.

2. Check the displayed waveforms and compare them with the waveforms shown in Figure 4.8.

Over compensated     Perfectly compensated     Under compensated

Figure 4.8 Probe Compensation

3. Use the probe compensation adjustment tool provided in the accessories to adjust the low-frequency compensation adjustment hole on the probe until the displayed waveform is consistent with the "Perfectly compensated" waveform shown in the above figure.

## 4.4 Product Overview

Unless otherwise specified, this chapter takes the four-channel model DHO814 as an example to introduce the appearance and dimensions, front and rear panels, and user interface of the DHO800 series oscilloscope.

### 4.4.1 Front Panel Overview

Figure 4.9 Front Panel (2-channel Model)

Figure 4.10 Front Panel (4-channel Model)
1. **7" Capacitive Touch Screen**

Displays the waveforms, menu labels, and parameter settings, system state, prompt messages, and other information.

2. **Multipurpose Knobs**

- **Non-menu operation:**
  When not operating on the menu, you can rotate the knob 1 to adjust the waveform brightness. When a cursor, decoding, Math waveform, or reference waveform is added on the screen, you can rotate the multipurpose knob to move the cursor (knob 1 and 2), adjust the decode threshold (knob 1) and decode result display position (knob 2), adjust the vertical scale (knob 1) and vertical offset (knob 2) of the math/reference waveform. You can click or tap **Flex Knob** on the Toolbar at the upper-right of the screen to set priority.
  - Automatic: Cursor > Math/Ref/Decode > Intensity (default priority).
  - Manual: all non-menu operation items are listed at the lower part of the **Flex Knob** menu. You can select one of them as the current item for multipurpose knob to adjust.

- **Menu operation:**
  When operating on the menu, you can rotate the multipurpose knob 1/2 to adjust the value in the menu. When you click or tap an input field and then the **1**/**2** icon is displayed in the input field, it indicates that you can use multipurpose knob 1/2 to set the value. The LED indicator of the corresponding knob is illuminated. At this point, you can rotate the knob to adjust the value or press the knob to restore the parameter to the default value.

When using the virtual numeric keypad or drop-down list, you can rotate the knob to navigate through the keypad or drop-down list and press the knob to select an item.

3. **Analyse Key**
Press to access the Analyse menu. In this menu, you can access analysis features including digital voltmeter (DVM), counter, power analysis, waveform recording, and pass/fail.

4. **Measure Key**

Press to access the Measure menu. You can select the waveform parameters in the menu. For details, refer to Select the Measurement Item.

5. **Cursor Key**

Press to enable cursor measurements. The results are displayed in the right-side "Result" bar. Three cursor modes are available: Manual, Track, and XY; wherein, the XY mode is available only when the XY function is enabled.

6. **Common Tools Keys**

- is the auto scale key. Press this key to enable the auto scale function. The oscilloscope is automatically configured to best display the input signals by adjusting the vertical scale, horizontal timebase, and trigger mode. To set up the key, please refer to Auto Config.

- is the RUN/STOP key. Press the key to set the oscilloscope's run state to "RUN" or "STOP". In "RUN" state, this key is illuminated in green; in "STOP" state, this key is illuminated in red.

- is the key for a single acquisition. Press this key to set the oscilloscope's trigger mode to "Single".

- is the default setup key. Press this key twice to directly restore the oscilloscope's default settings. You can also press the key and a dialog box is displayed. Click or tap OK in the dialog to restore the oscilloscope's default settings.

- is the clear key. Press this key to clear all waveform on the display. If the oscilloscope is in "RUN" mode, it continues to display new waveforms.

7. **Touch Lock Key**
is the touch lock key. Press this key once to disable the touch screen function; press it again to enable the touch screen.

8. **Quick Action Key**

Press to perform the selected quick action: print screen, save wave, save setup, measure all, statistics reset, waveform record, or save group. To set up the key, please refer to Quick Action Settings.

9. **Trigger Controls**

- is the trigger setup key. Press this key to access the Trigger menu. For details, please refer to Triggering the Oscilloscope.

- is the trigger slope setup key. Press this key to select the edge type (rising edge, falling edge, or either edge). This key is not active when the trigger type is not set to "Edge".

- is the force trigger key. Press this key to force a trigger.

- LEVEL is the trigger level/digital threshold knob. Turn the knob clockwise to increase the trigger level or turn the knob counterclockwise to decrease the level. Pressing the knob can quickly set the trigger level to the waveform's 50% peak-to-peak value.

10. **Horizontal Controls**

- Horizontal POSITION is the horizontal position knob. Turn the knob to change the horizontal position (trigger position) to move the waveforms horizontally. Press the knob to reset the horizontal position to default.

- Horizontal SCALE is the horizontal scale knob. Turn the knob to change the horizontal time/div setting to compress or expand waveforms of all channels horizontally. Press this knob to toggle between fine and coarse adjustment for horizontal time base or enable/disable the Zoom mode (related to Fine/Zoom)

- is the horizontal menu key. Press this key to access the Horizontal menu in which you can set the horizontal system and acquisition system.
- is the Navigate key. Press this key to access the Navigation menu. You can navigate time, search events, or segments. For details, please refer to Navigation.

- are the navigation keys. You can use the keys to navigate time, search events, or segments. You can also use the keys to play recorded waveforms.

11. **Vertical Controls**

- is the Math key. Press this key to access the Math menu. Math operations include A+B, A-B, A×B, A/B, FFT, etc. You can also set the Math label.

- is the reference key. Press this key to assess the Ref menu, in which you can add reference waveforms in waveform view and compare them with measured waveforms to identify circuit fault.

- Vertical POSITION is the vertical position knob. Turn this knob to change the selected waveform's vertical position to move the waveform up or down on the display. Press this knob to reset the vertical position to zero.

- Vertical SCALE is the vertical scale knob. Rotate this knob to modify the value of vertical divisions of the graticule in volts/div to increase or decrease the display amplitude of the waveform. Press this knob to toggle between fine and coarse adjustment of the vertical scale.

- / / / is the channel key. Depending on the actual situation, press the key to enable (display), select, or disable the corresponding channel, as described below:
  - If the channel is not displayed, you can press the channel key to open the channel in the waveform view window.
  - If the channel is displayed but not selected, you can press the channel key to select the channel.
  - If the channel is both displayed and selected, you can press the channel key to close its display in the waveform view.

**NOTE**

As DHO802/DHO812 is a two-channel model, it only provides two channel keys (**1** and **2**).

12. **Probe Compensation Signal Output Terminal/Ground Terminal**

This terminal outputs the probe compensation signal which helps you match a probe's input capacitance to the oscilloscope channel to which it is connected.

13. **External Trigger Input Terminal (for DHO812 and DHO802 only)**

BNC connector to input external trigger signal.

14. **Analog Channel Input Terminals**

BNC connectors. Attach probes to these connectors for analog signal inputs.

**NOTE**

As DHO802/DHO812 is a two-channel model, it only provides two analog input terminals.

15. **USB HOST Port**

This series supports USB storage device of FAT32/NTFS format and mouse.

- **USB storage device:** imports or exports data (software update, waveform, setup, or captured image).
- **Mouse:** connects a mouse to control the instrument.

16. **Power Key**

Powers on/off the oscilloscope.
### 4.4.2 Rear Panel Overview

Figure 4.11 Rear Panel

1. **AUX OUT**

- **Trigger output:**
  After the AUX output is set to "TrigOut", the oscilloscope generates a trigger and outputs a signal that can reflect the current capture rate of the oscilloscope via this interface. Connect the signal to a waveform display device and measure the frequency of the signal. The measurement result is the same as the current capture rate.

- **Pass/Fail:**
  After the AUX output is set to "PassFail", in the pass/fail test, the instrument will output a pulse via the [AUX OUT] connector when a passed or failed waveform is detected during the pass/fail test.

2. **LAN**

Connect the instrument to network via this interface. The instrument conforms to the standards specified in LXI Device Specification 2011. Its test system can be built quickly. Then you can control the instrument through using Web Control to send the SCPI commands. When update is available, you can perform online upgrading for the system software of the instrument via the LAN interface.

3. **USB DEVICE**

Connect the instrument to the PC via this interface. Then you can use the PC software to send the SCPI commands or use the user-defined programming to control the instrument.
4. **HDMI**

You can connect the instrument to an external display that has the HDMI interface (e.g. monitor or projector) via this interface to better observe the waveform display clearly. At this time, you can also view the waveforms on the LCD of the instrument.

5. **USB Type-C Power Connector**

The power requirements of the oscilloscope are DC, 15 V, 3 A. Please use the power adaptor provided in the accessories to connect the oscilloscope to the AC power source (100 V to 240 V, 50 Hz to 60 Hz).

6. **Security Lock Hole**

Use a standard PC/laptop lock cable to secure the oscilloscope to a work bench or other location.

7. **Ground Terminal**

Connect the instrument chassis to the ground using the lead.

8. **Mounting Screws**

Interval of screw holes: 100 mm x 100 mm. Use screws to secure the oscilloscope to the bracket with the same screw hole interval.

### 4.4.3 User Interface Overview

Figure 4.12 User Interface
1. **Waveform View**

Displays the measurement waveform window for CH1-CH4. Click or tap at the upper-right corner of the window to close the window; click or tap to enter the configuration menu of the specified function.

2. **Run State Label**

Displays the operating status of the instrument. Possibles states include RUN, STOP, T'D, WAIT, and AUTO.

3. **Horizontal Timebase Label**

Displays the current horizontal time base. Click or tap this label to enter the horizontal setting menu.

4. **Sample Rate & Memory Depth Label**

Displays the current sample rate and memory depth. Click or tap this label to enter the horizontal setting menu.

5. **Horizontal Position Label**

Displays the current horizontal position. Click or tap this label to enter the horizontal setting menu.

6. **Trigger Label**

- Displays the trigger information of the system, including the trigger type, trigger level, trigger mode, and etc.
- Click or tap the trigger label, then the trigger setting window is displayed. You can set the parameters for the trigger.

7. **Function Toolbar**

Provides STOP/RUN, Default, Measure, Flex Knob, Windows, Cursors, Math, XY, Storage, Counter, DVM, Decode, Record, and Navigate keys.

8. **Result Sidebar**

Displays the measurement results and statistics of various functions. Click or tap at the lower-right corner of the screen to open or close the "Result" sidebar.

9. **Split-screen Display**

If you enable multiple functions, multiple windows can be displayed on the screen at one time.

10. **Notification Area**

Displays USB icon, LAN icon, sound icon, and remote control icon. You can click or tap this area to open the "Utility" menu.
- USB storage device icon: When a USB storage device is detected, will be displayed.
- LAN icon: When the LAN interface is successfully connected, is displayed.

- Sound icon: In the "Utility" menu, click or tap Setup > Beeper to enable or disable the sound. When on, will be displayed; when off, will be displayed. You can simply click or tap the icon to enable or disable the sound.

- Remote control icon: When you use Web Control to control the instrument remotely, will be displayed.

11. **Math Labels**
- Displays the on/off states of Math1-Math4.
- Click or tap M1-M4 labels to display the on/off state, operation type, and vertical scale for Math1-Math4.

12. **Channel Labels**
- Display the channel on/off status.
- Display the channel coupling mode.
- Display the vertical scale.
- Display the vertical offset.
- Click or tap the label to enable/disable the corresponding channel or open the Vertical menu.

**NOTE**

As DHO802/DHO812 is a two-channel model, it only provides two channel labels.

13. **Function Navigation Icon**
Click or tap the icon to open the function navigation menu in which you can access the specified function menu by clicking or tapping the corresponding function key.

## 4.5 Touch Screen Gestures

The instrument provides a super large capacitive touch screen, which is convenient for users to operate and make configurations. It has strong waveform display capacity and excellent user experience. It features great convenience, high flexibility, and great
sensitivity. The actions supported by the touch screen controls include tapping, pinching&stretching, and dragging.

### 4.5.1 Tap

Use one finger to tap the symbol or characters on the screen slightly, as shown in Figure 4.13. With the Tap gesture, you can perform the following operations:

• Tap the menu displayed on the screen to operate on the menu.

• Tap the function navigation icon at the lower-left corner of the touch screen to enable the function navigation.

• Tap the displayed numeric keypad to set the parameters.

• Tap the virtual keypad to set the label name and the filename.

• Tap the close button at the upper-right corner of the message box to close the prompt window.

• Tap other windows on the touch screen and operate on the windows.

Figure 4.13 Tap Gesture

### 4.5.2 Drag

Use one finger to select the object, and then drag the object to a destination place, as shown in the figure below. With the drag gesture, you can perform the following operation:

• Drag the waveform to change its position or scale.

• Drag the window controls to change the position of the window (e.g. numeric keypad).

• Drag the cursor to move the cursor.

• Drag the trigger cursor to change the trigger level.

• In multi-window display, drag one of the displayed windows to change its position on the display.

Figure 4.14 Drag Gesture

### 4.5.3 Pinch&Stretch

Pinch or stretch two points on the screen with two fingers to zoom in or out the waveform. To zoom in the waveform, first pinch the two fingers and then stretch the fingers; to zoom out the waveform, first stretch the two fingers, and then pinch the fingers together, as shown in the figure below. With the pinch&stretch gesture, you can perform the following operation:

• Pinching&stretching in the horizontal direction can adjust the horizontal time base of the waveform.

• Pinching&stretching in the vertical direction can adjust the vertical scale of the waveform.

Figure 4.15 Pinch&Stretch Gesture

## 4.6 Parameter Setting Method

For this instrument, you can use the knob and touch screen to set parameters. The common parameter setting methods are as follows:

• **Method 1:** Some parameters can be adjusted by rotating the knob on the front panel.

• **Method 2:** Click or tap the input field of a specified parameter, then a virtual keypad is displayed. Complete the parameter setting with the keypad.

### Input Chinese and English Characters

When naming a label, this instrument supports Chinese/English input method. The following part introduces how to input Chinese and English characters with the Chinese/English input method.

• **Input English Characters**

Figure 4.16 English Input Interface

1. **Select English input method**

First check the input method type. If it shows "En/中", then go to Step 2; if it shows "中/En", click or tap the input method switchover key to switch to "En/中" (English input method).

2. **Clear the name input area**

If there is no character in the "Name Input Area", please go to the next step. If there are characters in the "Name Input Area", click or tap the Backspace key to delete all the characters from the "Name Input Area" in order.

3. **Input the upper-case letter**

If you want to input an upper-case letter, first use the Caps key to switch between the upper-case and lower-case mode. If the Caps key is selected, input the upper-case letter with the virtual keypad. If not, first click or tap the Caps key to ensure it is selected, then input the upper-case letter. All the input letters will be displayed in the "Name Input Area".

4. **Input the lower-case letter**

Refer to the operation specified in the previous step. If the Caps key is not selected, directly input the lower-case letter.

5. **Input numbers or symbols**

If the letter keypad is displayed, you need to click or tap the numeric switchover key to switch to the numeric keypad, and input numbers or symbols with the numeric keypad. All the input letters will be displayed in the "Name Input Area".

6. **Modify or delete the unwanted characters that have been input**

During the name input process, you can modify or delete the unwanted character if necessary. To delete the characters that have been input, click or tap the Backspace key in the virtual keypad to delete the characters. To modify the characters that have been input, delete the unwanted characters first and then input the new characters.

You can directly move the cursor to the character to be modified or deleted, delete the desired character or input the new characters after deleting the unwanted character.

7. **Confirm the input**

After completing the input operation, click or tap "OK".

• **Input Chinese Characters**

Figure 4.17 Chinese Input Interface

1. **Select Chinese input method**

First check the input method type. If it shows "中/En", then go to Step 2; if it shows "En/中", click or tap the input method switchover key to switch to "中/En" (Chinese input method).

2. **Clear the name input area**

If there is no character in the "Name Input Area", please go to the next step. If there are characters in the "Name Input Area", click or tap the Backspace key to delete all the characters from the "Name Input Area" in order.

If there are characters in the "Pinyin Input Area", when you delete characters from the name input area, the characters in the Pinyin input area will be deleted first.

3. **Input Chinese characters**

Click or tap the characters in the virtual keypad to input Pinyin into the input area, then the characters to be selected will be displayed in the Chinese character selection area. Slide to view more Chinese characters for you to choose. Select the desired Chinese character, and then the selected character will be displayed in the input area.

4. **Modify or delete the unwanted characters that have been input**

During the name input process, you can modify or delete the unwanted character if necessary. To delete the characters that have been input, click or tap the Backspace key in the virtual keypad to delete the characters. To modify the characters that have been input, delete the unwanted characters first and then input the new characters.

5. **Confirm the input**
After completing the input operation, click or tap "OK".

**Input a String**

When naming a file or folder, you need to input a string with the string keypad.

Figure 4.18 String Keypad

1. **Clear the name input area**

If there is no character in the "Name Input Area", please go to the next step. If there are characters in the "Name Input Area", click or tap the Backspace key to delete all the characters from the "Name Input Area" in order.

2. **Input the upper-case letter**

If you want to input an upper-case letter, first use the Caps key to switch between the upper-case and lower-case mode. If the Caps key is selected, input the upper-case letter with the virtual keypad. If not, first click or tap the Caps key to ensure it is selected, then input the upper-case letter. All the input letters will be displayed in the "Name Input Area".

3. **Input the lower-case letter**

Refer to the operation specified in the previous step. If the Caps key is not selected, directly input the lower-case letter.

4. **Input numbers or symbols**

If the letter keypad is displayed, you need to click or tap the numeric switchover key to switch to the numeric keypad, and input numbers or symbols with the numeric keypad. All the input letters will be displayed in the "Name Input Area".
5. **Modify or delete the unwanted characters that have been input**

During the name input process, you can modify or delete the unwanted character if necessary. To delete the characters that have been input, click or tap the Backspace key in the virtual keypad to delete the characters. To modify the characters that have been input, delete the unwanted characters first and then input the new characters.

You can directly move the cursor to the character to be modified or deleted, delete the desired character or input the new characters after deleting the unwanted character.

6. **Confirm the input**

After completing the input operation, click or tap "OK".

**Input a Value**

When setting or modifying a parameter, input an appropriate value with the numeric keypad.

• Click or tap the value or unit in the numeric keypad to complete the input.

• Rotate the multipurpose knob (1/2) to move the cursor to select the desired value and unit. Press the knob to confirm the input.

Figure 4.19 Numeric Keypad

After you input all the values and select the desired units, the numeric keypad is turned off automatically. This indicates that you have completed parameter setting. Besides, after you have input the values, you can also click or tap "OK" directly to close the numeric keypad. At this time, the unit of the parameter is the default unit. In the numeric keypad, you can perform the following operations:
• Modify the parameter value that has been input;
• Set the parameter value to a maximum or minimum value;
• Set the parameter to a default value;
• Clear the parameter input field.

## 4.7 To Use the Security Lock

If necessary, you can lock the instrument to a fixed location by using the security lock (please purchase it by yourself), as shown in the figure below.

The method is as follows: align the lock with the lock hole and plug it into the lock hole vertically, turn the key clockwise to lock the oscilloscope, and then pull the key out.

Security Lock Hole

Figure 4.20 To Use the Security Lock

**CAUTION**

Please do not insert other objects into the security lock hole to avoid damaging the instrument.

## 4.8 To Use the Built-in Help System

The built-in help file provides information about the functions and menu introductions of the instrument. Click or tap > Help to enter the help system.

In the help system, you can get its help information by clicking on or tapping the link for the specified chapter.

# 5 Vertical System

This series oscilloscope provides 2 analog input channels (CH1-CH2) for DHO802 and DHO812 and 4 analog input channels (CH1-CH4) for DHO804 and DHO814, and each channel is equipped with an independent vertical control system. The setting methods for their vertical systems are the same. This chapter takes CH1 of the four-channel model as an example to introduce the setting method for the vertical system.

When a channel is selected, click or tap the channel status label at the bottom of the screen. Then the menu as shown in the figure below is displayed.

Figure 5.1 Vertical Menu

## 5.1 To Enable or Disable the Analog Channel

**Enable the Analog Channel**

When a signal is connected to CH1, you can enable the channel in the following ways.

• Click or tap the channel status label at the bottom of the screen to enable the channel.

• Press the front-panel **1** key to enable the channel, and the backlight of this key is illuminated.

• In Figure 5.1, select the CH1 tab. Click or tap the Display on/off switch to turn CH1 on or off.

When CH1 is activated, its status label at the bottom of the screen is as shown in the figure below.

The information displayed in the channel status label is related to the current channel setting (irrelevant with the on/off status of the channel). After the channel is turned on, modify the parameters such as the vertical scale, horizontal time base, trigger mode, and trigger level according to the input signal for easy observation and measurement of the waveform.

When CH1 is enabled but not activated, its status label is as shown in the following figure.

Click or tap the channel status label at the bottom of the screen or press the front-panel **1** key to activate CH1. You can also select the CH1 tab in Vertical menu to activate it.

**Disable the Analog Channel**

You can disable the analog channel in the following ways.

• If CH1 has been enabled and activated, you can press the front-panel **1** key to disable it directly. You can also click or tap the channel status label at the bottom of the screen to open the Vertical menu and then click or tap the label again to disable the channel.

• If CH1 has been enabled but not activated, first activate the channel. Then press the front-panel **1** key or use the channel status label to disable CH1.

• In Figure 5.1, set Display to OFF to disable CH1.

• In addition, you can slide down the channel label to disable the channel.

If CH1 is disabled, its status label is as shown in the figure below.

## 5.2 To Adjust the Vertical Scale

Vertical scale indicates the voltage value per grid in the vertical axis of the screen. It is often expressed in V/div. Adjusting the vertical scale increases or decreases the display amplitude of the waveform. The scale information of the channel status label at the bottom of the screen would change accordingly.

The adjustable range of the vertical scale is related to the current probe ratio. By default, the probe ratio is 1X. In this case, the adjustable range of the vertical scale is from 500 μV/div to 10 V/div.

When CH1 is turned on and activated, you can adjust the vertical scale in the following ways.

• Rotate the Vertical **SCALE** knob to adjust the vertical scale (clockwise to reduce the scale and counterclockwise to increase).

• Enable the touch screen function, and then adjust the vertical scale with the pinch & stretch gesture on the touch screen. For details, refer to descriptions in Pinch&Stretch.

• In the Vertical menu, click or tap the icon at the right side of the input field of Scale to increase or decrease the scale value or use the corresponding multipurpose knob on the front panel to set the value. You can also click or tap the input field to input a specific value with the displayed numeric keypad.

In the Vertical menu, click or tap the Fine on/off switch to toggle between ON (fine adjustment) and OFF (coarse adjustment). The default setting is OFF. You can also press the Vertical **SCALE** knob to toggle between "coarse adjustment" and "fine adjustment".

• **Fine adjustment:** Use the icons at the right side of Scale or rotate the knob to further adjust the vertical scale within a relatively smaller range to improve vertical resolution. If the amplitude of the input waveform is a little bit greater than the full scale under the current scale and the amplitude would be a little bit lower if the next scale is used, fine adjustment can be used to improve the amplitude of waveform display to view signal details.

• **Coarse adjustment:** Use the icons at the right side of Scale or rotate the knob to adjust the vertical scale in a 1-2-5 step sequence, i.e. 500 μV/div, 1 mV/div, 2 mV/div, 5 mV/div, 10 mV/div...10 V/div.

## 5.3 To Adjust the Vertical Offset

Vertical offset indicates the offset of the signal ground level position of the waveform from the vertical center of the display. Its unit is consistent with the currently selected amplitude unit (refer to To Specify the Amplitude Unit). Adjusting the vertical offset moves the corresponding channel's waveform up and down. The vertical offset information (as shown in the following figure) in the channel status label at the bottom of the screen will change accordingly.

The adjustable range of the vertical offset is related to the current probe ratio and vertical scale.

When CH1 is turned on and activated, you can adjust the vertical offset in the following ways.

• Rotate the Vertical **POSITION** knob at the right section of the front panel to adjust the vertical offset within the adjustable range. Rotate this knob clockwise to increase the vertical offset, and rotate it counterclockwise to reduce the vertical offset. Pressing down the knob can quickly reset the vertical offset (set the vertical offset to 0).

• Enable the touch screen function, and then adjust the vertical offset with the drag gesture. For details, refer to Drag.

• In the Vertical menu, click or tap the Up/Down arrow icon at the right side of the input field of Offset to increase or decrease the offset value or use the corresponding multipurpose knob to set the value. You can also click or tap the input field to input a specific value with the pop-up numeric keypad.

## 5.4 To Specify Channel Coupling

You can remove unwanted signals by setting the coupling mode. For example, the signal under test is a square waveform with DC offset.

Click or tap the channel status label at the bottom of the screen, and then the Vertical menu is displayed. Click or tap the Coupling drop-down button to select the coupling mode.

• When the coupling mode is "DC", both the DC and AC components of the signal under test can pass the channel.

• When the coupling mode is "AC", the DC components of the signal under test are blocked.

• When the coupling mode is "GND", the DC and AC components of the signal under test are blocked.

After a coupling mode is selected, it is indicated in the channel status label at the bottom of the screen, as shown in the figure below.

DC                    AC                    GND

## 5.5 To Specify Bandwidth Limit

This oscilloscope supports the bandwidth limit function. Setting the bandwidth limit can reduce the noises in the displayed waveforms. For example, the signal under test is a pulse with high frequency oscillation.

• When the bandwidth limit is turned off, the high frequency components of the signal under test can pass the channel.

• When the bandwidth limit is turned on, the high frequency components found in the signal under test that are greater than the limit are attenuated. This series supports 20 MHz bandwidth limit.

Click or tap the channel status label at the bottom of the screen, and then the Vertical menu is displayed. Click or tap the BW Limit drop-down button to select the specified bandwidth. When the bandwidth limit is enabled, the specific bandwidth limit value will be displayed in the channel status label at the bottom of the screen, as shown in the figure below.

**TIP**

Bandwidth limit can not only reduce the noise, but also can attenuate or eliminate the high frequency components of the signal.

## 5.6 To Specify Input Impedance

This series oscilloscope provides 1 MΩ input impedance mode. In this mode, the input impedance of the oscilloscope is very high, and the current flowed from the circuit under test can be ignored.

## 5.7 To Invert a Waveform

Click or tap the channel status label at the bottom of the screen, and then the Vertical menu is displayed. Then click or tap the Invert on/off switch to enable or disable the waveform invert function.

When "ON" is selected, the channel label is as shown in the figure below.

When the Invert function is disabled, the waveform is displayed normally; when enabled, the voltage values of the displayed waveform are inverted, as shown in the figure below. Inverting a waveform also changes the result of math function, waveform measurement, etc.

Figure 5.2 Waveform Invert On/Off

**TIP**

When the Invert function is turned on, the trigger (e.g. Edge trigger, Pulse trigger, or Slope trigger) edge or polarity will be changed.

## 5.8 To Set Probe

The analog channel of this oscilloscope supports passive probes. For detailed technical information of the probes, please refer to the corresponding Probe User Guide.

Click or tap the channel status label at the bottom of the screen. Then the Vertical menu is displayed. Then click or tap Probe to enter the Probe setting menu, as shown in the figure below.

Figure 5.3 Probe Setting Menu

**Probe Ratio**

The oscilloscope allows you to set the probe attenuation manually. To obtain the accurate measurement results, you must set the probe ratio properly. By default, the probe ratio is 1X.

The probe ratio values available are as shown in the following table.

Table 5.1 Probe Ratio

| Menu | Attenuation (display amplitude of the signal: actual amplitude of the signal) |
|------|-----------------------------------------------------------------------------|
| 0.001X | 0.001:1 |
| 0.002X | 0.002:1 |
| 0.005X | 0.005:1 |
| 0.01X | 0.01:1 |
| 0.02X | 0.02:1 |
| 0.05X | 0.05:1 |
| 0.1X | 0.1:1 |
| 0.2X | 0.2:1 |
| 0.5X | 0.5:1 |
| 1X (default) | 1:1 |
| 2X | 2:1 |
| 5X | 5:1 |
| 10X | 10:1 |
| 15X | 15:1 |
| 20X | 20:1 |
| 50X | 50:1 |
| 100X | 100:1 |
| 150X | 150:1 |
| 200X | 200:1 |
| 500X | 500:1 |
| 1000X | 1000:1 |
| 1500X | 1500:1 |
| 2000X | 2000:1 |
| 5000X | 5000:1 |
| 10000X | 10000:1 |
| 15000X | 15000:1 |
| 20000X | 20000:1 |
| Menu | Attenuation (display amplitude of the signal: actual amplitude of the signal) |
|------|-----------------------------------------------------------------------------|
| 50000X | 50000:1 |

**Go Back to the Vertical Menu**

In the Probe setting menu, click or tap **Vertical** to go back to the Vertical menu.

## 5.9 To Specify the Amplitude Unit

Click or tap the channel status label at the bottom of the screen, and then the Vertical menu is displayed. Click or tap the Unit drop-down button to select W, A, V, or U. The default unit is V.

Changing the amplitude unit also changes the units of the functions related to the channel accordingly.

## 5.10 To Adjust Bias

When you use an oscilloscope to make actual measurements, a small offset that arises from the temperature drift of the component or external environment disturbance may occur on the zero-cross voltage of the channel, which will affect the measurement results of the vertical parameters. This series oscilloscope allows you to set an offset calibration voltage for calibrating the zero point of the corresponding channel so as to improve the accuracy of the measurement results.

In the "Vertical" menu, click or tap the Up/Down arrow icon at the right side of the input field of Bias to increase or decrease the bias value. You can click or tap the input field to set the value with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value.

The range of bias is related to the vertical scale.

**TIP**

If the zero-cross voltage of the channel has a larger amplitude offset that exceeds the adjustable range, please perform self-calibration for the instrument to ensure the measurement accuracy. For details, refer to SelfCal.

## 5.11 To Specify the Skew

When using an oscilloscope for actual measurement, the transmission delay of the probe cable may bring relatively greater errors (zero offset). This series oscilloscope allows you to set a delay time for calibrating the zero offset of the corresponding channel. Zero offset is defined as the offset of the crossing point of the waveform and trigger level line relative to trigger position, as shown in the figure below.

Figure 5.4 Zero Offset

In the "Vertical" menu, click or tap the Ch-Ch Skew input field to set the channel-to-channel skew time. The available range is from -100 ns to 100 ns, and the default is 0.00 s.

## 5.12 To Turn the Channel Label Display On/Off

The instrument uses the channel number to mark the corresponding channel by default. For ease of use, you can also set a label for each channel. For example, CH1.

Click or tap the channel status label at the bottom of the screen. Then the Vertical menu is displayed. Click or tap the Label on/off switch to turn the label display on or off. You can also click or tap the label input field to input a specific name for the channel label with the pop-up keypad.

For how to use the keypad, refer to descriptions in Parameter Setting Method.

# 6 Horizontal System

You can access the Horizontal menu in the following ways.

• Click or tap the channel status label at the bottom of the screen, and then the Vertical menu is displayed. Click or tap the Acquisition button to enter the Horizontal menu.

• Click or tap the horizontal time base label ("H" icon), acquisition label ("A" icon), or horizontal position label ("D" icon) at the top of the screen to enter the Horizontal menu.

• Press the front-panel **Menu** key to enter the Horizontal menu.

Figure 6.1 Horizontal Menu

## 6.1 To Adjust the Horizontal Time Base

Horizontal time base, also called the horizontal scale, refers to the time of each grid in the horizontal direction of the screen. It is usually expressed in s/div. The range of the horizontal time base is from 5.00 ns/div to 500 s/div.

While you change the horizontal time base, the displayed waveforms of all channels are expanded or compressed horizontally relative to the selected time reference (Horizontal Expansion Reference). The horizontal time base in the horizontal time base label ("H" icon) will change accordingly, as shown in the figure below.

You can adjust the horizontal time base in the following ways.

• Rotate the front-panel Horizontal **SCALE** knob to adjust the horizontal time base (clockwise to decrease the scale and counterclockwise to increase).

• Enable the touch screen function, and then adjust the horizontal time base with the Pinch&Stretch gesture. For details, refer to Pinch&Stretch.

• In the Horizontal menu, click or tap the icon at the right side of the input field of Scale to increase or decrease the horizontal time base or use the corresponding multipurpose knob to set the value. You can also click or tap the input field to input a specific value with the pop-up numeric keypad.

In the Horizontal menu, click or tap the Vernier on/off switch to toggle between ON (fine adjustment) and OFF (coarse adjustment). You can also press the front-panel Horizontal **SCALE** knob to toggle between "coarse adjustment" and "fine adjustment".

• **Coarse adjustment:** Click or tap the icons at the right side of the input field of Scale to adjust the horizontal time base of the waveforms of all channels in a 1-2-5 step sequence within the adjustable range.

• **Fine adjustment:** Click or tap the icon at the right side of the input field of Scale to adjust the horizontal time base of the waveforms of all channels at a smaller step within the adjustable range.

## 6.2 To Adjust the Horizontal Position

Horizontal position, also called trigger position, refers to the trigger point position of the waveforms of all channels in the horizontal direction relative to the center of the display. When the waveform trigger point is at the left (right) side of the center, the horizontal position is a positive (negative) value.

Changing the horizontal position moves the waveform trigger points and the displayed waveforms of all channels horizontally. The horizontal position displayed in the horizontal position label ("D" icon) changes accordingly, as shown in the figure below.

You can adjust the horizontal position in the following ways.

• Rotate the Horizontal **POSITION** knob at the right section of the front panel to adjust the horizontal position within the adjustable range. Rotate this knob clockwise to reduce the horizontal position or counterclockwise to increase the horizontal position. Pressing the knob can quickly reset the horizontal position (set the horizontal position to 0).

• Enable the touch screen function, and then adjust the horizontal position with the drag gesture. For details, refer to Drag.

• In the "Horizontal" menu, use the corresponding multipurpose knob to set the horizontal position or use the icons at the right side of the input field of Position to increase or decrease the value, as shown in the figure below. You can also click or tap the Position input field to input a specific value with the pop-up numeric keypad.

| Position | 0.00s | ⚡ | ◀ | ▶ |
|----------|-------|----|----|---|
|          | Input Field | | Increase | Decrease |

## 6.3 Zoom Mode (Delayed Sweep)

Zoom (delayed sweep mode) can be used to horizontally expand a length of waveform to view waveform details. In the Horizontal menu, click or tap the Zoom on/off switch to enable or disable the delayed sweep function. When it is enabled, you can set the scale and position in Zoom mode.

| Zoom | OFF | ON | | Vernier | OFF | ON |
|------|-----|----|-|---------|-----|-----|
| **Scale** | 1.00μs | ⚡ | 🔄 | **Position** | 0.00s | ◀ | ▶ |

| Input Field for Zoomed Time Base | Increase | Decrease | | Input Field for Zoomed Position | Increase | Decrease |
|----------------------------------|----------|----------|-|--------------------------------|----------|----------|

• **Zoomed Scale**: Rotate the corresponding multipurpose knob or use the icons at the right side of the Scale input field to increase or decrease the time base for the Zoom window. You can also click or tap the input field to input the specific value directly via the pop-up numeric keypad.

• **Zoomed Position**: Rotate the corresponding multipurpose knob or use the icons at the right side of the Position input field to increase or decrease the position for the Zoom window. You can also click or tap the input field to input the specific value directly via the pop-up numeric keypad.

When the Zoom mode is enabled, the display divides in half, as shown in the figure below.

Figure 6.2 Zoom Mode

• **Waveform before expansion:**

The upper portion of the display that is not covered by subtransparent gray shows the normal display of the waveform. Its horizontal time base (called the main time base) is indicated in the label at the upper-left corner of the display. You can move the area left and right by adjusting the horizontal position and increase or decrease the size of the area by adjusting the horizontal scale.

• **Waveform after expansion:**

The lower portion shows the horizontally expanded version of the normal waveform display. Its horizontal time base (called the zoomed time base) is displayed in the middle. Compared with the main time base, the zoomed time base has higher resolution.

**TIP**

The zoomed time base should be smaller than or equal to the main time base.

# 7 Acquisition System

The "Horizontal" menu allows you to configure the instrument's acquisition system.

Figure 7.1 Horizontal Menu

## 7.1 Acquisition Mode

The acquisition mode is used to determine how the waveform points are calculated from the sample points. In the Horizontal menu, click or tap the desired acquisition mode for the Acquisition item. This oscilloscope provides four acquisition modes: Normal (default), Average, Peak, and UltraAcquire. The selected acquisition mode is indicated in the acquisition label ("A" icon) at the top of the screen.

**Normal**

In Normal acquisition mode, the oscilloscope samples the signal at a fixed time interval to rebuild the waveform. This mode produces the best display for most waveforms.

**Average**

In this mode, the oscilloscope averages the waveforms from multiple acquisitions to reduce the random noise of the input signal and increase the vertical resolution. A greater number of averages lowers the noise and increases the vertical resolution. On the other hand, the higher the number of averages, the slower the response of the displayed waveform to waveform changes.

When you select "Average" mode, click or tap the Averages input field to set the number of averages with the pop-up numeric keypad or use the corresponding multipurpose knob to set the value. Its range is from 2 to 65536, and the default is 2.

**NOTE**

The number of averages must be the Nth power of 2. When it is not in N power-of-2 increments, a prompt message "Truncation average error" is displayed. At this time, a value that is smaller than the one you input and the closest to N power-of-2 increments will be input automatically.

**Peak**

In this mode, the oscilloscope acquires the maximum and minimum values of the signal within the acquisition interval to get the signal envelope or capture narrow pulses that might be lost. This mode prevents signal aliasing at the expense of exaggerating the noise.

In this mode, the minimum pulse width detected is the sample period.

**UltraAcquire**

UltraAcquire mode is one of the fast acquisition modes. It divides the oscilloscope's memory into segments and fills a memory segment for each individual trigger event. It provides a much higher waveform capture rate and helps minimize the dead time between trigger events.

When you select "UltraAcquire" mode, click or tap the Display Frame input field to set the number of frames and the Timeout input field to set the timeout. When the number of the frames reaches the maximum or the sampling time reaches the timeout, the oscilloscope stops sampling and plots the waveform. Click or tap the Display mode drop-down button to select the display mode of the acquired data.

• Adjacent: Waveform segments are shown in an adjacent way with each segment shown next to the previous segment in time order. A maximum of 100 frames can be displayed on the screen at a time in this mode.

• Overlay: All the captured waveform segments are overwritten to display as one single segment of the waveform. A maximum of 100 frames can be displayed on the screen at a time in this mode.

• Waterfall: It displays the captured waveform segments in a cascaded display order. A maximum of 100 frames can be displayed on the screen at a time in this mode.

• Perspective: The waveform segments are displayed in the ladder-like form, with each segment being arranged above another with a certain perspective (angle), moving up like a rising slope. A maximum of 100 frames can be displayed on the screen at a time in this mode.
• Mosaic: The whole waveform view is divided into several blocks, and each waveform segment is displayed in each block in sequence. A maximum of 80 frames can be displayed on the screen at a time in this mode.

Figure 7.2 Display Modes

**TIP**

• The UltraAcquire mode is not available when any of the following functions is enabled: cursors, decoding, Search, Zoom, Pass/Fail test, waveform recording, reference waveform, roll mode, slow sweep mode, and XY mode. To switch to the UltraAcquire mode, please ensure that all of those functions are disabled.

• In UltraAcquire mode, the functions mentioned above (except for roll mode and slow sweep mode) are disabled. When roll mode or slow sweep mode is enabled, the acquisition mode is automatically switched to "Normal".

## 7.2 Sampling Mode

This oscilloscope only supports the real-time sampling mode. In this mode, the oscilloscope produces the waveform display from samples collected during one trigger event. The maximum real-time sample rate of this series is 1.25 GSa/s. The current sample rate is displayed in the acquisition label at the top of the screen.

By default, the operating status label at the left top of the screen is illuminated in green, indicating that the instrument is in real-time sampling, and the STOP/RUN button on the toolbar is in green. Click or tap the STOP/RUN button or press the front-panel key to stop sampling. At this time, the operating status label shows "STOP" in red, and the STOP/RUN button turns red. Also, the backlight of the front-panel key turns red. The oscilloscope will maintain its last captured graph. You can still pan or zoom the waveforms by using the horizontal/vertical controls.

## 7.3 Sample Rate

Sampling is the process of converting an analog signal into digital data at a specified time interval and then storing them sequentially in acquisition memory. The sample rate is the reciprocal of the time interval.

In Horizontal menu, the "SaRate" item shows the current sample rate. The current sample rate is also indicated in the acquisition label ("A" icon) at the top of the screen, as shown in the figure below.

Sample Rate

Sample Interval

The sample rate of the analog channel is related to the instrument model and current channel mode. For two-channel models (DHO802 and DHO812), the oscilloscope provides up to 1.25 GSa/s real-time sample rate in single channel mode and 625 MSa/s real-time sample rate in all channels mode. For four-channel models (DHO814 and DHO804), the oscilloscope provides up to 1.25 GSa/s real-time sample rate in single channel mode, 625 MSa/s real-time sample rate in half channels mode, and 312.5 MSa/s real-time sample rate in all channels mode.

• **Single channel mode**: If any one of the channels is enabled, it is called single channel mode.

• **Half channels mode**: For four-channel models, if two of the channels are enabled, it is called half channels mode.

• **All channels mode**: For two-channels models, if all two channels are enabled, it is called all channels mode; for four-channel models, if any three channels or all four channels are enabled, it is called all channels mode.

A sample rate that is too low might have the following effects on the waveform:

• **Waveform Distortion**: When the sample rate is too low, some waveform details are lost, and the sample waveform displayed is rather different from the actual waveform of the signal.

• **Waveform Aliasing**: Aliasing occurs when the sample rate is twice lower than the actual signal frequency (Nyquist Frequency). The frequency of the waveform reconstructed from the sample data is smaller than the actual signal frequency.

• **Waveform Leakage**: If the sample rate is too low, the waveform reconstructed from the sample data does not represent the original signal correctly.

## 7.4 Memory Depth

Memory depth refers to the number of points that the oscilloscope can store in a single trigger acquisition. It reflects the storage capability of the acquisition memory. This series oscilloscope provides up to 25 Mpts memory depth (standard).

Figure 7.3 Memory Depth

The following formula shows the relations among memory depth, sample rate, and horizontal time base:

MDepth ≥ SRate x TSCale x HDivs

• MDepth indicates the memory depth. The unit is pts.

• SRate indicates the sample rate. The unit is Sa/s.

• TSCale indicates the horizontal time base. The unit is s/div.

• HDivs indicates the number of grids in the horizontal direction. The unit is div.

Therefore, with the same horizontal time base, a higher memory depth can ensure a higher sample rate.

In Horizontal menu, click or tap the Mem Depth drop-down button to select the memory depth. The default setting is "10k". The selected memory depth value is displayed in the acquisition label ("A" icon) at the top of the screen.

• When only one of the channels is enabled, the memory depths available include Auto, 1 kpts, 10 kpts, 100 kpts, 1 Mpts, 5 Mpts, 10 Mpts, and 25 Mpts.

• When two of the channels are enabled, the memory depths available include Auto, 1 kpts, 10 kpts, 100 kpts, 1 Mpts, 5 Mpts, and 10 Mpts.

• When three channels or all four channels are enabled (only available for four-channel models), the memory depths available include Auto, 1 kpts, 10 kpts, 100 kpts, 1 Mpts, and 5 Mpts.

**TIP**

• In "Auto" mode, the oscilloscope selects the memory depth automatically according to the current sample rate.

• When Acquisition Mode is set to "Average", the maximum memory depth available is 10 Mpts in single channel mode and 1 Mpts in half channels mode/all channels mode.

## 7.5 Horizontal Expansion Reference

This function allows you to set the position that the waveform on the display is referenced to when it is horizontally expanded or compressed when the horizontal time base is adjusted. In the Horizontal menu, click or tap the Expand drop-down button to select the reference position. Available options include Center (default), Left, Right, Trigger, and User.

• Center: when the horizontal time base is modified, the waveform will be expanded or compressed horizontally relative to the center of the display.
• Left: when the horizontal time base is modified, the waveform will be expanded or compressed horizontally relative to the leftmost position of the display.

• Right: when the horizontal time base is modified, the waveform will be expanded or compressed horizontally relative to the rightmost position of the display.

• Trigger: when the horizontal time base is modified, the waveform will be expanded or compressed horizontally relative to the trigger point.

• User: when the horizontal time base is modified, the waveform will be expanded or compressed horizontally relative to the user-defined reference position.

When you select "User", click or tap the User Expansion input field and set the value with the displayed numeric keypad. Its range is from -500 to 500, and the default is 0.

## 7.6 Roll Mode

The roll mode causes the waveform to move across the screen from right to left. It allows you to view the acquired data without waiting for a complete acquisition. In Horizontal menu, select "Auto" or "OFF" in Roll.

• Auto: the Roll mode is enabled. It is automatically enabled when the horizontal scale is 50 ms/div or slower.

• OFF: the Roll mode is disabled. The oscilloscope operates at slow sweep speeds when the horizontal scale is 200 ms/div or slower. In slow sweep mode, the oscilloscope acquires the data to the left of the trigger point and then waits for trigger. After the trigger occurs, it continues to acquire the data to the right of the trigger point. When you use this mode to observe low-frequency signals, it is recommended to set the channel coupling mode (To Specify Channel Coupling) to "DC".

**TIP**

• If the Zoom mode is currently turned on, enabling the roll mode automatically turns off the Zoom mode.

• The following functions are not available when the roll mode is enabled: To Adjust the Horizontal Position (available when the oscilloscope run state is STOP), Zoom Mode (Delayed Sweep), Triggering the Oscilloscope, Protocol Decoding, Pass/Fail Test, Waveform Recording and Playing, Persistence Time, UltraAcquire, Average, XY Mode, Search.

## 7.7 XY Mode

By default, this series oscilloscope uses the YT mode for waveform display window. In YT mode, Y-axis indicates the Voltage and X-axis indicates the Time. Besides, it also
supports the XY display in which both X-axis and Y-axis indicate voltage. The XY mode converts the oscilloscope from a "Voltage-Time" display to a "Voltage-Voltage" display using two input channels.

**Enable the XY Mode**

You can enable the XY display mode in the following ways.

• Click or tap the Windows button in the function navigation menu or on the toolbar to enter the Add Window menu. In the "Diagram" item, click or tap XY > Add to enable the XY display mode.

• Click or tap the XY button in the function navigation menu or on the toolbar to enable the XY display mode.

• In the "Horizontal" menu, tick XY to enable the XY mode.

**Configure the XY Mode**

Click or tap at the upper-right corner of the XY display window to enter the XY configuration menu.

Figure 7.4 XY Menu

• Source: Click or tap the drop-down button of "Source X" to select the source channel of the X-axis in the XY window. Click or tap the drop-down button of "Source Y" to select the source channel of the Y-axis in the XY window.

In the Add Window menu, you can also configure Source Z. Source Z, as the Z-axis input in the XY display mode, is used to control whether to display the X-Y waveforms in the XY display mode. This function is called "blanking".
- When "None" is selected for "Source Z", the blanking function is disabled, and you can only see the X-Y waveforms.
- When you select "CH1-CH4" for "Source Z", the blanking function is enabled. The Z-axis input from the external connector determines whether to display the X-Y waveforms. When Z is high (the input level is greater than 0 V), the X-Y waveforms are displayed; when Z is low (the input level is smaller than 0 V), the waveforms are hidden.

• Grid: Please refer to To Set the Screen Grid.

**NOTE**

Advanced settings are not available for now. The current settings can produce the best display.

**Phase Deviation Measurement**

In this mode, you can use the Lissajous method to measure the phase deviation of the two input signals whose frequencies are the same. The following figure shows the measurement schematic diagram of phase deviation.

Figure 7.5 Measurement Schematic Diagram of Phase Deviation

According to sinƟ=A/B or C/D, Ɵ is the phase deviation angle between the two channels. The definitions of A, B, C, and D are shown in the figure above. The phase deviation angle is obtained, that is:

Ɵ=±arcsin(A/B) or ±arcsin(C/D)

If the principal axis of the ellipse is within Quadrant I and III, the phase deviation angle obtained should be within Quadrant I and IV, namely within (0 to π/2) or (3π/2 to 2π). If the principal axis of the ellipse is within Quadrant II and IV, the phase deviation angle obtained should be within Quadrant II and III, namely within (π/2 to π) or (π to 3π/2).
The XY mode can be used to measure the phase deviation occurred when the signal under test passes through a circuit network. Connect the oscilloscope to the circuit to monitor the input and output signals of the circuit.

# 8 Triggering the Oscilloscope

The trigger system allows you to set specific trigger conditions as required. The oscilloscope captures a waveform as well as its neighboring part and displays them on the screen once a particular trigger condition is met. For a digital oscilloscope, it samples waveform continuously no matter whether it is stably triggered. Rather, only stable triggering can produce stable display. The trigger module ensures that every time base sweep or acquisition starts from the user-defined trigger condition, namely every sweep is synchronous with the acquisition and the waveforms acquired are overlapped so as to display the stable waveforms.

You should set the triggers based on the features of the input signal. To quickly capture your desired waveforms, you need to understand the signal under test. This oscilloscope provides a variety of trigger types that help you focus on the desired waveform details.

You can enter the Trigger menu in the following ways.

• Press the front-panel **Trigger** key to enter the trigger menu.

• In Figure 5.1, click or tap the Trigger button to enter the trigger menu.

• Click or tap the trigger label (as shown in the figure below) at the top of the screen to enter the trigger menu.

## 8.1 Trigger Source

In the "Trigger" menu, click or tap the drop-down button of Source to select the desired source. Available sources include analog channels CH1-CH4 and EXT.

**Analog Channel Input**

Signals input from analog channels CH1-CH4 can all be used as trigger sources. No matter whether the channel selected is enabled, the channel can work normally.

**External Trigger Input (for DHO812 and DHO802 only)**

The external trigger source can be used to trigger on the third channel while both the channels are acquiring data. The trigger signal (e.g. external clock or signal of the circuit under test) will be connected to EXT trigger source via the external trigger input terminal [EXT TRIG] connector. You can set the trigger conditions within the range of the trigger level (from -5 V to +5 V).
## 8.2 Trigger Level

The adjustment of the trigger level/threshold level is related to the type of the trigger source.

• When the trigger source is CH1-CH4, rotate the front-panel LEVEL knob or use the corresponding multipurpose knob (when the trigger menu is opened) to adjust the trigger level. You can also click or tap the Level input field to set the value with the pop-up numeric keypad. During the adjustment, a trigger level line (the color of the trigger level line is the same as that of the channel) and a trigger icon "T" are displayed on the screen, and they move up and down with the variation of the trigger level. When you stopping modifying the trigger level, the trigger level line disappears in about 2 s. The current trigger level is displayed in the trigger information label at the top of the screen.

In Runt Trigger, Slope Trigger, and Window trigger, you need to set the upper and lower limits of the trigger level. Two trigger level icons T1 and T2 are displayed at the right section of the screen.

• When the trigger source is EXT, rotate the front-panel LEVEL knob or use the corresponding multipurpose knob (when the trigger menu is opened) to adjust the trigger level. You can also click or tap the Level input field to set the value with the pop-up numeric keypad. The current trigger level is displayed in the trigger information label at the top of the screen.

For this trigger source, only the variation of the trigger level value is displayed on the screen during the adjustment of the trigger level, without displaying the trigger level lines on the screen.

To better trigger the waveforms, for a trigger with a single level, you can directly click or tap 50% in the menu or press the trigger level knob to make the level move to the middle of the waveform. However, for a trigger with two levels (e.g. Slope trigger, Runt trigger, Window trigger), you need to click or tap 90% for Level A and 10% for Level B to make the level move within the range of the waveform amplitude.

## 8.3 Trigger Mode

The following is the schematic diagram of the acquisition memory. To better understand the trigger event, you can think of the trigger event as dividing acquisition memory into a pre-trigger and post-trigger buffer.
After the oscilloscope starts running, it first fills the pre-trigger buffer. Then, after the pre-trigger buffer is filled, the oscilloscope starts searching for a trigger. While searching for the trigger, the data sampled will still be transmitted to the pre-trigger buffer (the new data will continuously overwrite the previous data). When a trigger is found, the pre-trigger buffer contains the events that occurred just before the trigger. Then, the oscilloscope will fill the post-trigger buffer and display the data in the acquisition memory. If the acquisition is initiated via the front-panel **RUN/STOP** key, the process repeats; if the acquisition is initiated via the **SINGLE** key, it stops after finishing a single acquisition (you can pan and zoom the currently displayed waveform).

This series provides Auto (default), Normal, and Single trigger modes.

Click or tap the trigger information label (as shown in the figure below) at the top of the screen or press the front-panel **Trigger** key to open the "Trigger" menu. In the Sweep item, you can quickly switch the current trigger mode. The selected trigger mode is displayed in the trigger information label at the top of the screen: A (Auto), N (Normal), or S (Single).

• **Auto:** In this trigger mode, if the specified trigger conditions are not found, triggers are forced and acquisitions are made so that signal activity is displayed on the oscilloscope. This trigger mode can be used when the signal levels are unknown, when the DC signals should be displayed, or when trigger conditions occur often enough that forced triggers are unnecessary.

• **Normal:** In this trigger mode, triggers and acquisitions only occur when the specified trigger conditions are found. This trigger mode can be used when the signal is at a low repetition rate, when you only want to acquire specific events specified by the trigger settings, or when you try to stabilize the display by preventing the oscilloscope from auto-triggering.

• **Single:** In this trigger mode, a single trigger and acquisition only occur when the specified trigger conditions are found, and then the oscilloscope stops.
trigger mode can be used when you need to make a single acquisition of the specified event and analyze the acquisition result. You can pan and zoom the currently displayed waveform without subsequent waveform data overwriting the current waveform. After a single trigger is initiated, the oscilloscope is in "STOP" state.

In Normal and Single trigger modes, you can click or tap the Force button in the trigger menu or press the front-panel key to force a trigger event.

## 8.4 Trigger Coupling

Trigger coupling determines what part of the signal is passed to the trigger circuit. Please distinguish it from channel coupling (To Specify Channel Coupling). This function is available only when the trigger type is Edge and the trigger source is an analog channel.

In the "Trigger" menu, click or tap the Coupling drop-down button to select the desired coupling mode (by default, it is DC).

• DC: allows DC and AC components to pass the trigger circuitry.

• AC: blocks the DC components and attenuates the signals.

• LFR: blocks the DC components and rejects the low-frequency components.

• HFR: rejects the high frequency components.

**TIP**

When "AC" or "LFR" is selected as the coupling mode, no trigger level lines and trigger icons are displayed. When you adjust the trigger level, you can only see the changes of the trigger level values in the trigger information label at the top of the screen.

## 8.5 Trigger Holdoff

Trigger holdoff can be help stabilize triggering on complex repetitive waveforms that have multiple edges or other events between waveform repetitions (such as pulse series). Holdoff time is specified as the amount of time that the oscilloscope waits for re-arming the trigger circuitry after generating a correct trigger. The oscilloscope will not trigger even if the trigger condition is met during the holdoff time and will only re-arm the trigger circuitry after the holdoff time expires.
For example, to get a stable trigger on the repetitive pulse burst as shown in the figure below, set the holdoff time to be greater than t1 but less than t2.

Figure 8.2 Trigger Holdoff

Click or tap the trigger information label (as shown in the figure below) at the top of the screen or press the front-panel **Trigger** key to open the "Trigger" menu. Click or tap the input field of Holdoff to set the holdoff time (the holdoff to this time when the waveforms are stably triggered) with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. The adjustable range of the holdoff time is from 8 ns (default) to 10 s.

## 8.6 Noise Rejection

Noise rejection can reject the high frequency noise in the signal and reduce the possibility of triggering the oscilloscope by mistake.

Click or tap the trigger information label (as shown in the figure below) or press the front-panel **Trigger** key to open the "Trigger" menu. Click or tap the Noise Reject on/off switch to enable or disable the noise rejection function.

## 8.7 Trigger Type

This series oscilloscope provides the following trigger types.
### 8.7.1 Edge Trigger

Edge trigger identifies a trigger on the trigger level of the specified edge on the input signal.

**Trigger Type**

Click or tap the Type drop-down button to select "Edge".

Figure 8.3 Edge Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including the trigger type, source, and level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4 or EXT(for two-channel models only). For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Edge Type**

In the Slope item, select which edge of the input signal will trigger the oscilloscope. The selected slope will be indicated in the trigger information label.
• Rising: triggers on the rising edge of the input signal when the voltage level meets the specified trigger level.

• Falling: triggers on the falling edge of the input signal when the voltage level meets the specified trigger level.

• Either: triggers on the rising or falling edge of the input signal when the voltage level meets the preset trigger level.

**TIP**

When edge trigger is selected, you can also press the front-panel **Slope** key to switch the edge type.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Trigger Coupling, Trigger Holdoff, and Noise Rejection to set the coupling, trigger holdoff, and noise rejection under this trigger type.

**Trigger Level**

Click or tap the Level input field to set the trigger level with the pop-up numeric keypad. You can also use the front-panel trigger level knob or the corresponding multipurpose knob to set the trigger level. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

### 8.7.2 Pulse Width Trigger

Pulse width triggering sets the oscilloscope to trigger on the positive or negative pulse of a specified width. In this mode, the oscilloscope will trigger when the pulse width of the input signal satisfies the specified pulse width condition.

In this oscilloscope, positive pulse width is defined as the time difference between the two crossing points of the trigger level and positive pulse; negative pulse width is defined as the time difference between the two crossing points of the trigger level and negative pulse, as shown in the figure below.
Figure 8.4 Positive/Negative Pulse Width

**Trigger Type**

Click or tap the Type drop-down button to select "Pulse".

Figure 8.5 Pulse Width Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including the trigger type, source, and level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.
**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Polarity**

In the Polarity item, select the desired polarity: positive polarity ( ) or negative polarity ( ).

**Trigger Condition**

Set the trigger condition in the When item.

• When you select "Positive" for polarity, ">" for trigger condition, the oscilloscope triggers when the positive pulse width of the input signal is greater than the specified pulse width.

• When you select "Positive" for polarity, "<" for trigger condition, the oscilloscope triggers when the positive pulse width of the input signal is smaller than the specified pulse width.

• When you select "Positive" for polarity, "< >" for trigger condition, the oscilloscope triggers when the positive pulse width of the input signal is greater than the specified lower limit of pulse width and smaller than the specified upper limit of pulse width.

• When you select "Negative" for polarity, ">" for trigger condition, the oscilloscope triggers when the negative pulse width of the input signal is greater than the specified pulse width.

• When you select "Negative" for polarity, "<" for trigger condition, the oscilloscope triggers when the negative pulse width of the input signal is smaller than the specified pulse width.

• When you select "Negative" for polarity, "< >" for trigger condition, the oscilloscope triggers when the negative pulse width of the input signal is greater than the specified lower limit of pulse width and smaller than the specified upper limit of pulse width.

**Pulse Width Setting**

• In the When menu, when ">" or "<" is selected, click or tap the input field of Upper or lower to set the upper limit value or the lower limit value with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. The pulse width available is from 1 ns to 10 s.
• In the When menu, when "< >" is selected, click or tap the input field of Upper and Lower respectively to set the upper limit value and the lower limit value with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the values. The lower limit of the pulse width must be smaller than the upper limit.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Trigger Holdoff and Noise Rejection to set the trigger holdoff and noise rejection under this trigger type.

**Trigger Level**

Click or tap the Level input field to set the trigger level with the pop-up numeric keypad. You can also use the front-panel trigger level knob or the corresponding multipurpose knob to set the trigger level. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

### 8.7.3 Slope Trigger

Slope triggering sets the oscilloscope to trigger on the positive or negative slope of the specified time. This trigger mode is applicable to ramp and triangle waveforms.

In this oscilloscope, positive slope time is defined as the time difference between the two crossing points of trigger level line A and B with the rising edge; negative slope time is defined as the time difference between the two crossing points of trigger level line A and B with the falling edge. See the figure below.

Figure 8.6 Positive Slope Time/Negative Slope Time

**Trigger Type**

Click or tap the Type drop-down button to select "Slope".
Figure 8.7 Slope Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including trigger type, trigger source, and trigger level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Edge Type**

Select the input signal edge (in the Slope item) on which the oscilloscope triggers.

• Rising: triggers on the rising edge of the input signal.

• Falling: triggers on the falling edge of the input signal.

**Trigger Condition**

Set the trigger condition in the When item.
• When you select "Rising" for the edge type, ">" for trigger condition, the oscilloscope triggers when the positive slope time of the input signal is greater than the specified time.

• When you select "Rising" for the edge type, "<" for trigger condition, the oscilloscope triggers when the positive slope time of the input signal is smaller than the specified time.

• When you select "Rising" for the edge type, "< >" for trigger condition, the oscilloscope triggers when the positive slope time of the input signal is greater than the specified lower limit time and smaller than the specified upper limit time.

• When you select "Falling" for the edge type, ">" for trigger condition, the oscilloscope triggers when the negative slope time of the input signal is greater than the specified time.

• When you select "Falling" for the edge type, "<" for trigger condition, the oscilloscope triggers when the negative slope time of the input signal is smaller than the specified time.

• When you select "Falling" for the edge type, "< >" for trigger condition, the oscilloscope triggers when the negative slope time of the input signal is greater than the specified lower limit time and smaller than the specified upper limit time.

**Slope Time Setting**

• In the When item, when ">" or "<" is set to trigger conditions, click or tap the input field of Lower or Upper to set the lower limit value or the upper limit value with the pop-up numeric keypad. You can also use the corresponding knob to set the value. The slope time available is from 1 ns to 10 s.

• In the When item, when "< >" is set to trigger conditions, click or tap the input field of Upper and Lower respectively to set the upper limit value and the lower limit value with the pop-up numeric keypad. You can also use the corresponding knob to set the values. The lower slope time limit must be smaller than the upper slope time limit.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Trigger Holdoff and Noise Rejection to set the trigger holdoff and noise rejection under this trigger type.
**Level Selection and Setting**

After the trigger condition setting is completed, you need to adjust the trigger level to correctly trigger the signal and obtain a stable waveform.

Click or tap the Level A/Level B input field to set the level A/level B with the pop-up numeric keypad. You can also use the trigger level knob or use the corresponding multipurpose knob to adjust level A/level B. When Linkage is ticked, the upper limit and lower limit values change at the same time. The difference between upper and lower limit remains unchanged. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

**TIP**

Press the trigger level knob to switch between three modes: "only adjust Level A", "only adjust Level B", and "adjust Level A and Level B at the same time".

### 8.7.4 Video Trigger

The video signal can include image information and timing information, which adopts different standards and formats. This series can trigger on the standard video signal field or line of NTSC (National Television Standards Committee), PAL (Phase Alternating Line), or SECAM (Sequential Couleur A Memoire).

**Trigger Type**

Click or tap the Type drop-down button to select "Video".

Figure 8.8 Video Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including trigger type, trigger source, and trigger level) is displayed in the trigger information
label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Video Polarity**

In the Polarity item, select the desired polarity: positive polarity ( ) or negative polarity ( ).

**Video Standard**

Click or tap the drop-down button of Standard to select the desired video standard.

Table 8.1 Video Standard

| Video Standard | Frame Frequency (Frame) | Scan Type | TV Scan Line |
|----------------|-------------------------|-----------|--------------|
| NTSC | 30 | Interlaced Scan | 525 |
| PAL/SECAM | 25 | Interlaced Scan | 625 |
| 480p/60Hz | 60 | Progressive Scan | 525 |
| 576p/50Hz | 50 | Progressive Scan | 625 |
| 720p/60Hz | 60 | Progressive Scan | 750 |
| 720p/50Hz | 50 | Progressive Scan | 750 |
| 720p/30Hz | 30 | Progressive Scan | 750 |
| 720p/25Hz | 25 | Progressive Scan | 750 |
| 720p/24Hz | 24 | Progressive Scan | 750 |
| 1080p/60Hz | 60 | Progressive Scan | 1125 |
| 1080p/50Hz | 50 | Progressive Scan | 1125 |
| 1080p/30Hz | 30 | Progressive Scan | 1125 |
| 1080p/25Hz | 25 | Progressive Scan | 1125 |
| 1080p/24Hz | 24 | Progressive Scan | 1125 |
| 1080i/60Hz | 60 | Interlaced Scan | 1125 |
| 1080i/50Hz | 50 | Interlaced Scan | 1125 |
**Sync**

In the Sync item, select the desired sync type.

• All Lines: triggers on the first line found.

• Line: triggers on the specified line.

When this sync type is selected, you can specify a line number. Click or tap the input field of Line to set the line number by using the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. The range of the line number is related to the currently selected video standards. The range is from 1 to 525 (NTSC), 1 to 625 (PAL/SECAM), 1 to 525 (480p), 1 to 625 (576p), 1 to 750 (720p), or 1 to 1125 (1080p/1080i).

• Odd: triggers on the rising edge of the first ramp pulse in the odd field. It is only available when the video standard is set to "NTSC" or "PAL/SECAM".

• Even: triggers on the rising edge of the first ramp pulse in the even field. It is only available when the video standard is set to "NTSC" or "PAL/SECAM".

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Noise Rejection to set the noise rejection under this trigger type.

**Trigger Level**

Click or tap the Level input field to set the trigger level with the pop-up numeric keypad. You can also use the front-panel trigger level knob or the corresponding multipurpose knob to set the trigger level. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

**TIP**

• To better observe the waveform details in the video signal, you can set a larger memory depth first.

• In the trigger debugging process of video signals, the frequency in different part of the signal can be reflected by a different brightness, as RIGOL's digital oscilloscope provides the intensity graded color display function. Experienced users can quickly judge the signal quality and discover abnormalities during the debugging process.

### 8.7.5 Pattern Trigger

The pattern trigger identifies a trigger condition by looking for a specified pattern. This pattern is a logical "AND" combination of channels. Each channel can be set to H (high), L (low), or X (don't care). A rising or falling edge (you can only specify a single
edge) can be specified for one channel included in the pattern. When an edge is specified, the oscilloscope will trigger at the edge specified if the pattern set for the other channels are true (namely the actual pattern of the channel is the same as the preset pattern). If no edge is specified, the oscilloscope will trigger on the last edge that makes the pattern true. If all the channels in the pattern are set to "X", the oscilloscope will not trigger.

Figure 8.9 Pattern Trigger

**Trigger Type**

Click or tap the Type drop-down button to select "Pattern".

Figure 8.10 Pattern Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including the trigger type, source, and level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.
**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Pattern Setting**

The following five patterns are available:

• 1: sets the pattern of the channel selected to "1", i.e. the voltage level is higher than the trigger level of the channel.

• 0: sets the pattern of the channel selected to "0", i.e. the voltage level is lower than the trigger level of the channel.

• X: sets the pattern of the channel selected to "X", i.e. this channel is not used as a part of the pattern. When all channels in the pattern are set to "X", the oscilloscope will not trigger.

• ↗: sets the pattern to the rising edge of the channel selected.

• ↘: sets the pattern to the falling edge of the channel selected.

The Left/Right arrow key indicates moving left/right to switch the channel pattern. "All" indicates all bits. Select a pattern for a channel and then click or tap All. The patterns of all the other channels will be set to the currently selected pattern.

Only one edge (rising or falling edge) can be specified in the pattern. If one edge item is currently defined and then another edge item is defined in another channel in the pattern, then a prompt message "Invalid input" is displayed.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Trigger Holdoff and Noise Rejection to set the trigger holdoff and noise rejection under this trigger type.

**Trigger Level**

Click or tap the Level input field to set the trigger level with the pop-up numeric keypad. You can also use the front-panel trigger level knob or the corresponding multipurpose knob to set the trigger level. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.
### 8.7.6 Duration Trigger

In duration trigger, the oscilloscope identifies a trigger condition by searching for the duration of a specified pattern. This pattern is a logical "AND" combination of the channels. Each channel can be set to 1 (high), 0 (low), or X (don't care). The instrument triggers when the duration (∆T) of this pattern meets the preset time, as shown in the figure below.

Figure 8.11 Duration Trigger

**Trigger Type**

Click or tap the drop-down button of Type to select "Duration".
Figure 8.12 Duration Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including the trigger type, source, and level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Pattern Setting**

The following three patterns are available:

• 1: sets the pattern of the channel selected to "1", i.e. the voltage level is higher than the trigger level of the channel.

• 0: sets the pattern of the channel selected to "0", i.e. the voltage level is lower than the trigger level of the channel.

• X: sets the pattern of the channel selected to "X", i.e. this channel is not used as a part of the pattern. When all channels in the pattern are set to "X", the oscilloscope will not trigger.
The Left/Right arrow key indicates moving left/right to switch the channel pattern. "All" indicates all bits. Select a pattern for a channel and then click or tap All. The patterns of all the other channels will be set to the currently selected pattern.

**Trigger Condition**

Set the trigger condition in the When item.

• **>**: triggers when the duration of the pattern is greater the preset time. Click or tap the input field of Lower to set the lower limit of the duration of the pattern with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. The available range is from 1 ns to 10 s.

• **<**: triggers when the duration of the pattern is smaller than the preset time. Click or tap the input field of Upper to set the upper limit of the duration of the pattern. You can also use the corresponding multipurpose knob to set the value. The available range is from 1 ns to 10 s.

• **< >**: triggers when the duration of the pattern is smaller than the upper limit of the preset time and greater than the lower limit of the preset time. Click or tap the input field of Upper to set the upper limit of the duration of the pattern, and the range is from 1.01 ns to 10 s. Click or tap the input field of Lower to set the lower limit of the duration of the pattern, and the range is from 1 ns to 9.9 s. You can also use the corresponding multipurpose knob to set the upper/lower limit. The lower time limit must be smaller than the upper time limit.

• **> <**: triggers when the duration of the pattern is greater than the upper limit of the preset time or smaller than the lower limit of the preset time. Click or tap the input field of Upper to set the upper limit of the duration of the pattern, and the range is from 1.01 ns to 10 s. Click or tap the input field of Lower to set the lower limit of the duration of the pattern, and the range is from 1 ns to 9.9 s. You can also use the corresponding multipurpose knob to set the upper/lower limit. The lower time limit must be smaller than the upper time limit.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Trigger Holdoff and Noise Rejection to set the trigger holdoff and noise rejection under this trigger type.

**Trigger Level**

Click or tap the Level input field to set the trigger level with the pop-up numeric keypad. You can also use the front-panel trigger level knob or the corresponding multipurpose knob to set the trigger level. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.
### 8.7.7 Timeout Trigger

In Timeout trigger, the oscilloscope triggers when the time interval (∆T) (the time from when the rising edge (or falling edge) of the input signal passes through the trigger level to the time from when the neighboring falling edge (or rising edge) passes through the trigger level) is greater than the preset timeout value, as shown in Figure 8.13.

Figure 8.13 Timeout Trigger

**Trigger Type**

Click or tap the Type drop-down button to select "Timeout".

Figure 8.14 Timeout Trigger Menu

After a trigger type is selected, the current trigger setting information (including the trigger type, source, and level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.
**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Edge Type**

In Slope item, select the edge type from which the input signal passes through the trigger level.

• Rising: starts timing when the rising edge of the input signal passes through the trigger level.

• Falling: starts timing when the falling edge of the input signal passes through the trigger level.

• Either: starts timing when either edge of the input signal passes through the trigger level.

**Timeout Value**

Timeout value represents the maximum time that the signal remains idle before the signal passes through the trigger level. Click or tap the input field of Timeout, and then use the pop-up numeric keypad to set the timeout value of Timeout trigger. You can also use the corresponding multipurpose knob to set the value.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Noise Rejection to set the noise rejection under this trigger type.

**Trigger Level**

Click or tap the Level input field to set the trigger level with the pop-up numeric keypad. You can also use the front-panel trigger level knob or the corresponding multipurpose knob to set the trigger level. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.
### 8.7.8 Runt Trigger

The runt trigger sets the oscilloscope to trigger pulses that cross one trigger level but not another, as shown in the figure below.

Figure 8.15 Runt Trigger

**Trigger Type**

Click or tap the drop-down button of Type to select "Runt".

Figure 8.16 Runt Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including the trigger type, source, and level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.
**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Polarity**

Select the pulse polarity of Runt trigger under the Polarity item.

• Positive: indicates that the instrument triggers on the positive runt pulse.

• Negative: triggers on the negative runt pulse.

**Trigger Condition**

Set the Runt trigger condition in the When item.

• None: indicates not setting the trigger condition of Runt trigger.

• >: triggers when the runt pulse width is greater the Lower limit of pulse width. Click or tap the input field of Lower to set the minimum pulse width of Runt trigger with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to modify the value.

• <: triggers when the runt pulse width is smaller than the upper limit of pulse width. Click or tap the input field of Upper to set the maximum pulse width of Runt trigger with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to modify the value.

• < >: triggers when the runt pulse width is greater than the lower limit and smaller than the upper limit of pulse width. Click or tap the input field of Upper to set the maximum pulse width of Runt trigger with the pop-up numeric keypad. Click or tap the input field of Lower to set the minimum pulse width of Runt trigger with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to modify the maximum and minimum pulse width. The lower limit of the pulse width must be smaller than the upper limit.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Trigger Holdoff and Noise Rejection to set the trigger holdoff and noise rejection under this trigger type.
**Level Selection and Setting**

After the trigger condition setting is completed, you need to adjust the trigger level to correctly trigger the signal and obtain a stable waveform.

Click or tap the Level A/Level B input field to set the level A/level B with the pop-up numeric keypad. You can also use the trigger level knob or use the corresponding multipurpose knob to adjust level A/level B. When Linkage is ticked, the upper limit and lower limit values change at the same time. The difference between upper and lower limit remains unchanged. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

**TIP**

Press the trigger level knob to switch between three modes: "only adjust Level A", "only adjust Level B", and "adjust Level A and Level B at the same time".

### 8.7.9 Window Trigger

Window trigger provides a high trigger level and a low trigger level. The instrument triggers when the input signal passes through the high trigger level or the low trigger level.

**Trigger Type**

Click or tap the Type drop-down button to select "Over".

Figure 8.17 Window Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including trigger type, trigger source, and trigger level) is displayed in the trigger information
label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Edge Type**

Select the input signal edge (in the Slope item) on which the oscilloscope triggers.

• Rising: triggers on the rising edge of the input signal when Position condition is met.

• Falling: triggers on the falling edge of the input signal when Position condition is met.

• Either: triggers on the rising or falling edge of the input signal when Position condition is met.

**Trigger Position**

After selecting the window type, specify the time point of trigger by selecting the trigger position (in Position item).

• Enter: triggers when the input signal enters the specified trigger level range.

• Exit: triggers when the input signal exits the specified trigger level range.

• Time: triggers when the accumulated hold time since the input signal entered the specified trigger level range is equal to the window time. After you select this type, click or tap the input field of Time to set it by using the pop-up numeric keypad. The available range is from 1 ns to 10 s.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Trigger Holdoff and Noise Rejection to set the trigger holdoff and noise rejection under this trigger type.
**Level Selection and Setting**

After the trigger condition setting is completed, you need to adjust the trigger level to correctly trigger the signal and obtain a stable waveform.

Click or tap the Level A/Level B input field to set the level A/level B with the pop-up numeric keypad. You can also use the trigger level knob or use the corresponding multipurpose knob to adjust level A/level B. When Linkage is ticked, the upper limit and lower limit values change at the same time. The difference between upper and lower limit remains unchanged. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

**TIP**

Press the trigger level knob to switch between three modes: "only adjust Level A", "only adjust Level B", and "adjust Level A and Level B at the same time".

### 8.7.10 Delay Trigger

In Delay trigger, you need to set Source A and Source B. The oscilloscope triggers when the time difference (∆T) between the specified edges (Edge A and Edge B) of Source A and Source B meets the preset time limit, as shown in the figure below. Edge A and Edge B must be two neighboring edges.

Figure 8.18 Delay Trigger

**Trigger Type**

Click or tap the Type drop-down button to select "Delay".
Figure 8.19 Delay Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including trigger type, trigger source, and trigger level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Source Setting**

• **Source A**

Click or tap the drop-down button of SourceA to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

• **Edge A**

Select the trigger edge type ("Rising" or "Falling") of Source A in Delay trigger in the EdgeA item.

• **Source B**

Click or tap the drop-down button of SourceB to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.
Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

• **Edge B**

Select the trigger edge type ("Rising" or "Falling") of Source B in Delay trigger in the EdgeB item.

**Set the Trigger Condition**

Set the time limit condition of Delay trigger in the when item.

• **>**: triggers when the time difference (∆T) between the specified edges of Source A and Source B is greater than the preset time lower limit. Click or tap the input field of Lower to set the delay time lower limit in Delay trigger with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value.

• **<**: triggers when the time difference (∆T) between the specified edges of Source A and Source B is smaller than the preset time upper limit. Click or tap the input field of Upper to set the delay time upper limit in Delay trigger with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value.

• **< >**: triggers when the time difference (∆T) between the specified edges of Source A and Source B is greater than the lower limit of the preset time and smaller than the upper limit of the preset time. Click or tap the input field of Upper to set the delay time upper limit in Delay trigger with the pop-up numeric keypad. Click or tap the input field of Lower to set the delay time lower limit in Delay trigger with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the upper and lower limit. The lower time limit must be smaller than the upper time limit.

• **> <**: triggers when the time difference (∆T) between the specified edges of Source A and Source B is smaller than the lower limit of the preset time or greater than the upper limit of the preset time. Click or tap the input field of Upper to set the delay time upper limit in Delay trigger with the pop-up numeric keypad. Click or tap the input field of Lower to set the delay time lower limit in Delay trigger with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the upper and lower limit. The lower time limit must be smaller than the upper time limit.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Trigger Holdoff and Noise Rejection to set the trigger holdoff and noise rejection under this trigger type.
**Level Selection and Setting**

After the trigger condition setting is completed, you need to adjust the trigger level to correctly trigger the signal and obtain a stable waveform.

Click or tap the Level A/Level B input field to set the level A/level B with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to adjust level A/level B or use the trigger level knob to adjust the level (the focus of the trigger level knob is the last modified level). For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

### 8.7.11 Setup/Hold Trigger

In setup&hold trigger, you need to set the clock source and data source. The setup time starts when the data signal passes the trigger level and ends at the coming of the specified clock edge; the hold time starts at the coming of the specified clock edge and ends when the data signal crosses the trigger level again, as shown in the figure below. The oscilloscope triggers when the setup time or hold time is smaller than the preset time.

Figure 8.20 Setup/Hold Trigger

**Trigger Type**

Click or tap the drop-down button of Type to select "Setup/Hold".
Figure 8.21 Setup/Hold Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including the trigger type, source, and level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Clock Source**

Click or tap the drop-down button of SCL to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Edge Type**

Select the desired clock edge type in the Slope item, and it can be set to "Rising" or "Falling".

**Data Source**

Click or tap the drop-down button of SDA to select CH1-CH4. For details, refer to Trigger Source The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.
**Data Type**

Select the effective pattern of the data signal in the Data Type item. It can be set to H (high level) or L (low level).

**Trigger Condition**

Set the Setup/Hold trigger condition in the When item.

• **Setup**: the oscilloscope triggers when the setup time is smaller than the specified setup time. After selecting this type, click or tap the input field of Setup to set the setup time with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value.

• **Hold**: the oscilloscope triggers when the hold time is smaller than the specified hold time. After selecting this type, click or tap the input field of Hold to set the hold time with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value.

• **Setup/Hold**: the oscilloscope triggers when the setup time or hold time smaller than the specified time value. After selecting this type, click or tap the input field of Setup and Hold respectively to set the setup and hold time with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the values.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Trigger Holdoff and Noise Rejection to set the trigger holdoff and noise rejection under this trigger type.

**Level Selection and Setting**

After the trigger condition setting is completed, you need to adjust the trigger level to correctly trigger the signal and obtain a stable waveform.

Click or tap the Level A/Level B input field to set the level A/level B with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to adjust level A/level B or use the trigger level knob to adjust the level (the focus of the trigger level knob is the last modified level). For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

### 8.7.12 Nth Edge Trigger

The Nth edge trigger lets you to trigger on the Nth edge that occurs after a specified idle time. For example, in the waveform as shown in the figure below, the instrument should trigger on the second rising edge after the specified idle time (the time
between two neighboring rising edges), and the idle time should be within the range between P and M (P < Idle Time < M). Wherein, M is the time between the first rising edge and its previous rising edge; P is the maximum time between the rising edges that participate in counting.

Figure 8.22 Nth Edge Trigger

**Trigger Type**

Click or tap the Type drop-down button to select "Nth Edge".

Figure 8.23 Nth Edge Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including trigger type, trigger source, and trigger level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.
**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Edge Type**

Select the input signal edge (in the Slope item) on which the oscilloscope triggers.

• Rising: triggers on the rising edge of the input signal when the voltage level meets the specified trigger level.

• Falling: triggers on the falling edge of the input signal when the voltage level meets the specified trigger level.

**Idle Time**

Click or tap the input field of Idle Time, and then use the pop-up numeric keypad to set the idle time before the edge counting in Nth edge trigger. You can also use the corresponding multipurpose knob to set the value.

**Edge Count**

Click or tap the input field of Edges, then use the pop-up numeric keypad to set the value of "N" in Nth edge trigger. You can also use the corresponding multipurpose knob to set the value. The available range is from 1 to 65,535.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Noise Rejection to set the noise rejection under this trigger type.

**Trigger Level**

Click or tap the Level input field to set the trigger level with the pop-up numeric keypad. You can also use the front-panel trigger level knob or the corresponding multipurpose knob to set the trigger level. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.
### 8.7.13 RS232 Trigger

RS232 bus is a serial communication mode used in data transmission between PCs or between a PC and a terminal. In RS232 serial protocol, a character is transmitted as a frame of data. The frame consists of 1 start bit, 5-8 data bits, 1 check bit, and 1-2 stop bits. Its format is as shown in the figure below. This series oscilloscope triggers when detecting the start frame, error frame, check error, or the specified data of the RS232 signal.

Start Bit Data Bit Check Bit Stop Bit
1 bit 5~8 bits 1 bit 1~2 bits
Figure 8.24 Schematic Diagram of RS232 Protocol

Trigger Type

Click or tap the drop-down button of Type to select "RS232".

Figure 8.25 RS232 Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including the trigger type, source, and level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.
**Source Selection**

Click or tap the Source drop-down button to select CH1-CH4. For details, refer to Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Polarity**

Select the polarity of data transmission in the Polarity item. It can be set to "Positive" or "Negative".

**Trigger Condition**

Set the desired trigger condition in the When item.

• Start: triggers on the start frame position.

• Error: triggers when an error frame is detected.

• Check Error: triggers when a check error is detected.

• Data: triggers on the last bit of the preset data bits. Click or tap the input field of Data, and then use the pop-up numeric keypad to set the data of RS232 trigger. You can also use the corresponding multipurpose knob to set the value.

**Baud Rate**

You can select the baud rate of data transmission (i.e. specifies a clock frequency). Click or tap the drop-down button of Baud Rate, then select the preset baud rate. The available baud rates include 50 bps, 75 bps, 110 bps, 134 bps, 150 bps, 300 bps, and etc. You can also self-define the baud rate.

**Data Bits**

Indicates the number of bits per frame. Click or tap the drop-down button of Data Bits to select the desired data bits. The available data bits include "5 Bits", "6 Bits", "7 Bits", and "8 Bits".

**Stop Bit**

Indicates when to stop outputting data. Select the desired stop bit in the Stop Bit item. The available data bits include 1 Bit, 1.5 Bits, and 2 Bits.
**Parity**

Used to check whether the data are properly transmitted. Select None, Even, or Odd in the Parity item.

• None: indicates that no check bit appears during the transmission.

• Even: indicates that the total number of "1" in the data bit and check bit is an even number. For example, when 0x55 (01010101) is sent, "0" should be added to the check bit.

• Odd: indicates that the total number of "1" in the data bit and check bit is an odd number. For example, when 0x55 (01010101) is sent, "1" should be added to the check bit.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Noise Rejection to set the noise rejection under this trigger type.

**Trigger Level**

Click or tap the Level input field to set the trigger level with the pop-up numeric keypad. You can also use the front-panel trigger level knob or the corresponding multipurpose knob to set the trigger level. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

### 8.7.14 I2C Trigger

I2C is a 2-wire serial bus used to connect the microcontroller and its peripheral device. It is a bus standard widely used in the microelectronic communication control field.

The I2C serial bus consists of SCL and SDA. Its transmission rate is determined by SCL, and its transmission data is determined by SDA, as shown in the figure below. The instrument triggers on the start condition, restart, stop, missing acknowledgment, specific device address, or data value. Besides, it can also trigger on the specific device address and data values at the same time.
Figure 8.26 Sequence Diagram of I2C Protocol

**Trigger Type**

Click or tap the drop-down button of Type to select "I2C".

Figure 8.27 I2C Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including the trigger type, source, and level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Source Selection**

Click or tap the drop-down buttons of SCL and SDA to select CH1-CH4 to specify the sources of SCL and SDA respectively. For details, refer to descriptions in Trigger
Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Trigger Condition**

Set the desired trigger condition in the When item.

• Start: triggers when SDA data transitions from high level to low level while SCL is high level.

• Stop: triggers when SDA data transitions from low level to high level while SCL is high level.

• Restart: triggers when another start condition occurs before a stop condition.

• MissedAck: triggers when ACK is 1.

• Address: the trigger searches for the specified address value. When this event occurs, the oscilloscope will trigger on the read/write bit. After this trigger condition is selected:
  - Click or tap the drop-down button of Direction to select "Write", "Read", or "R/W".
  
  This setting is not available when AddrBits is set to "8 Bits".
  
  - Click or tap the drop-down button of AddrBits to select the desired address bits. The available address bits are "7 Bits", "8 Bits", and "10 Bits".
  
  - Click or tap the input field of Address, and then use the pop-up numeric keypad to set the address of I2C trigger. You can also use the corresponding multipurpose knob to set the value.

• Data: the trigger searches for the specified data value on the data line (SDA). When this event occurs, the oscilloscope will trigger on the clock line (SCL) transition edge of the last bit of data. After this trigger condition is selected, you can set the following parameters.
  
  - Click or tap the drop-down button of AddrBits to select the desired address bits. The available address bits are "7 Bits", "8 Bits", and "10 Bits".
  
  - Click or tap the input field of Bytes, and then use the pop-up numeric keypad to set the length of the data. You can also use the corresponding multipurpose knob to set the value. Its range is from 1 to 5.
  
  - Click or tap the input field of Data, and then the "Format" interface is will displayed. You can select "Bin" or "Hex" data format.
Figure 8.28 Binary Format Setting

Figure 8.29 Hexadecimal Format Setting

• **A&D**: the oscilloscope searches for the specified address and data at the same time, then triggers when both the address and data meet the conditions. After this condition is selected, you need to set the sub Data-menu items such as Direction, Bytes, AddrBits, Address, and Data. For the setting methods, refer to descriptions in "Address" and "Data" conditions.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.
**Trigger Parameter Setting**

You can refer to Noise Rejection to set the noise rejection under this trigger type.

**Level Selection and Setting**

After the trigger condition setting is completed, you need to adjust the trigger level to correctly trigger the signal and obtain a stable waveform.

• **Level A**

Click or tap the input field of Level A to input the level of SCL with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. When the level A information is displayed in the trigger label, you can also use the trigger level knob to adjust the level of SCL. For details, refer to descriptions in Trigger Level.

• **Level B**

Click or tap the input field of Level B to input the level of SDA with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. When the level B information is displayed in the trigger label, you can also use the trigger level knob to adjust the level of SDA. For details, refer to descriptions in Trigger Level.

### 8.7.15 SPI Trigger

In SPI trigger, after the CS or timeout condition is satisfied, the oscilloscope triggers when the specified data is found. When using SPI trigger, you need to specify the CLK clock sources and MISO data sources.

The figure below shows the sequential chart of SPI bus.

Figure 8.30 Sequential Chart of SPI Bus

**Trigger Type**

Click or tap the drop-down button of Type to select "SPI".
Figure 8.31 SPI Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including trigger type, trigger source, and trigger level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Source Selection**

Click or tap the drop-down buttons of CLK and MISO to select CH1-CH4 to specify the sources of CLK and MISO respectively. For details, refer to descriptions in Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Edge Type**

Select the desired clock edge type in Slope.

• Rising: samples the MISO data on the rising edge of the clock.

• Falling: samples the MISO data on the falling edge of the clock.

**Trigger Condition**

Select the desired trigger condition in When.
• With CS: if the CS signal is valid, the oscilloscope will trigger when the data (SDA) satisfying the trigger conditions is found.

  - Click or tap the drop-down button of CS to select CH1-CH4 as the CS signal line.

  - After selecting this condition, you can click or tap "Positive" (high level is valid) or "Negative" (low level is valid) in CS Mode.

• Timeout: the oscilloscope starts to search for the data (MISO) on which to trigger after the clock signal (CLK) stays in the idle state for a specified period of time. After selecting this condition, you can click or tap the Timeout input field, then use the numeric keypad to set the idle time. You can also use the corresponding multipurpose knob to set the value. The range is from 8 ns to 10 s.

**NOTE**

As DHO812/DHO802 only has two channels, the "With CS" is not available.

**Data**

Click or tap the of field of Data, and then the "Format" interface is displayed. You can set the data bit that needs to be triggered. For details, refer to descriptions in I2C Trigger.

**Data Bits**

Click or tap the input field of DataBits, and then use the pop-up numeric keypad to set the number of bits in the serial data string. You can also use the corresponding multipurpose knob to set the value. The number of bits in the string can be set to any integer ranging from 4 to 32.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Noise Rejection to set the noise rejection under this trigger type.

**Level Selection and Setting**

After the trigger condition setting is completed, you need to adjust the trigger level to correctly trigger the signal and obtain a stable waveform.

• **Level A**

Click or tap the input field of Level A to input the level of CLK with the pop-up numeric keypad. You can also use the corresponding multipurpose knob or the trigger level knob to adjust the level of CLK. When the level A information is displayed in the trigger label, you can also use the trigger level knob to adjust
the level of CLK. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

• **Level B**

Click or tap the input field of Level B to input the level of MISO with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to adjust the level of MISO. When the level B information is displayed in the trigger label, you can also use the trigger level knob to adjust the level of MISO. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

• **Level C**

Click or tap the input field of Level C to input the level of CS with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to adjust the level of CS. When the level C information is displayed in the trigger label, you can also use the trigger level knob to adjust the level of CS. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

### 8.7.16 CAN Trigger

This series oscilloscope can trigger on the start of a frame, end of a frame, frame of the specified type (e.g. Remote, Overload, Data), or error frame of the specified type (e.g. Answer Error, Check Error, Format Error) of the CAN signal.

The data frame format of the CAN bus is as shown in the figure below.

Figure 8.32 Data Frame Format of the CAN Bus

**Trigger Type**

Click or tap the drop-down button of Type to select "CAN".
Figure 8.33 CAN Trigger Setting Menu

After a trigger type is selected, the current trigger setting information (including trigger type, trigger source, and trigger level) is displayed in the trigger information label at the top of the screen, as shown in the figure below. The information will change based on the trigger settings.

**Source Selection**

Click or tap the drop-down button of Source to select CH1-CH4. For details, refer to descriptions in Trigger Source. The selected trigger source is indicated in the trigger information label at the top of the screen.

Only when you select the channel that has signal inputs as the trigger source, can you obtain a stable trigger.

**Signal Type**

Click or tap the drop-down button of Signal Type to select the desired signal type.

• CAN_H: indicates the actual CAN_H bus signal.

• CAN_L: indicates the actual CAN_L bus signal.

• TX/RX: indicates the Transmit signal and Receive signal from the CAN bus transceiver.

• DIFF: indicates the CAN differential bus signals connected to an analog channel by using a differential probe. Connect the probe's positive lead to the CAN_H bus signal and connect the negative lead to the CAN_L bus signal.
**Baud Rate**

Click or tap the drop-down button of Baud to select the preset baud rate. The available baud rates include 10 kbps, 20 kbps, 33.3 kbps, 50 kbps, 62.5 kbps, 83.3 kbps, and etc. You can also self-define the baud rate.

**Sample Position**

Sample position is a point within a bit's time. The oscilloscope samples the bit level at this point. The sample position is represented by the proportion of "the time from the start of the bit to the sample position" to the "bit time", as shown in the figure below.

Figure 8.34 Sample Position

Click or tap the input field of Sample Position to set it by using the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. The settable range is from 10% to 90%.

**Trigger Condition**

Click or tap the drop-down button of When to select the desired trigger condition.

• SOF: triggers at the start of a frame.

• EOF: triggers at the end of a frame.

• Remote ID: triggers on the specified ID of Remote frame. When you select Remote ID, you need to set the following parameters.

  - Click or tap the Extended ID on/off switch to enable or disable the extended ID.

  - Click or tap the input field of ID, and then the "Format" interface is displayed. You can set the ID that needs to be operated on. For details, refer to descriptions in I2C Trigger.

• Overload: triggers on the overload frames.

• Frame ID: triggers on the data frames with the specified ID. After you select Frame ID, you can refer to the "Remote ID" mentioned above to set the Extended ID and ID.

• Frame Data: triggers on the data frames with the specified Data. When you select Frame Data, you need to set the following parameters.
- Click or tap the input field of Data, and then the "Format" interface is displayed. You can set the data bit that needs to be operated on. For details, refer to descriptions in I2C Trigger.

- Click or tap the input field of Bytes, and then use the pop-up numeric keypad to set the length of the data. You can also use the corresponding multipurpose knob to set the value. Its range is from 1 to 8.

• Data&ID: triggers on the data frames with the specified ID and data. When you select Data&ID, you need to set the ID, Extended ID, Data, and Bytes.

• Frame Error: triggers on the error frame.

• Bit Fill: triggers on the error frame with the bit fill.

• Answer Error: triggers on the answer error frame.

• Check Error: triggers on the check error frame.

• Format Error: triggers on the format error frame.

• Random Error: triggers on the random error frame, such as the format error frame, answer error frame, etc.

**Trigger Mode**

In Sweep, select Auto, Normal, or Single as the trigger mode. For details, refer to descriptions in Trigger Mode.

**Trigger Parameter Setting**

You can refer to Noise Rejection to set the noise rejection under this trigger type.

**Trigger Level**

Click or tap the Level input field to set the trigger level with the pop-up numeric keypad. You can also use the front-panel trigger level knob or the corresponding multipurpose knob to set the trigger level. For details, refer to descriptions in Trigger Level. The current trigger level is displayed in the trigger information label at the top of the screen.

## 8.8 Trigger Output Connector

The rear-panel trigger output connector ([AUX OUT]) of this series can output trigger signals determined by the current setting (hardware trigger).

Click or tap > Utility. Click or tap Setup, and then select "TrigOut" in Aux Out. A signal which reflects the current oscilloscope capture rate can be output from [AUX OUT] connector each time a trigger is generated by the oscilloscope. If this signal is connected to a waveform display device to measure the frequency, the measurement result is the same as the current capture rate.
If "PassFail" is selected in Aux Out, the instrument can output a pulse from the [AUX OUT] connector when a pass/failed event is detected during the pass/fail test.

# 9 Math Operation

This series oscilloscopes can realize multiple math operations between waveforms of different channels, including arithmetic operation, spectrum operation, logic operation, function operation, and digital filter. You can access the Math menu in the following ways.

• Click or tap the function navigation icon at the lower-left corner of the screen, and then select Math to enter the "Math" menu.

• Click or tap the Math button on the toolbar at the upper-right corner of the screen to enter the "Math" menu.

• Click or tap M1-M4 in the Math label at the bottom of the screen to open the "Math" window. You can also click or tap the Math label and then select a label from M1-M4 to enter the corresponding Math window. Then click or tap the M1-M4 label again, or the icon at the upper-right corner of the window to enter the "Math" menu. The Math label is as shown in the figure below.

• Press the front-panel key to enter the "Math" menu.

Figure 9.1 Math Menu

This oscilloscope provides four math operations: Math1, Math2, Math3, and Math4. In the Math menu, you can select the desired math operation type by clicking or
tapping the Math1-Math4 label or by sliding the menu left and right. This manual takes Math1 as an example to introduce math operation.

In the Math menu, click or tap the Operation on/off switch to show or hide the waveform display window of the operation results. By default, it is OFF. When "ON" is selected for Math1-Math4, the menu as shown in the figure below is displayed on the screen.

Figure 9.2 Waveform Display Window of the Operation Results

You can drag the title bar of the display window to change the position of the window. You can also click or tap at the upper-right corner of the window to close it.

## 9.1 Arithmetic Operation

In the Math menu, click or tap the Operator drop-down button to select the desired math operation. The arithmetic operations supported by this oscilloscope include A+B, A-B, A×B, and A÷B.

• A+B adds the waveform voltage values of signal source A and B point by point and displays the results.

• A-B subtracts the waveform voltage values of signal source B from that of source A point by point and displays the results.

• A×B multiplies the waveform voltage values of signal source A and B point by point and displays the results.

• A÷B divides the waveform voltage values of signal source A by that of source B point by point and displays the results. It can be used to analyze the Multiple relation of the two channels waveforms.
**TIP**

When the voltage of signal source B is 0 V, the division result is treated as 0.

Figure 9.3 Arithmetic Operation Menu

**Operation Result Display Window**

Click or tap the Operation on/off switch to enable the display of the arithmetic operation result window. The source and the vertical scale parameters are displayed at the top of the window, as shown in the figure below.

Figure 9.4 Operation Result Display Window
**Source**

Click or tap the drop-down button of SourceA or SourceB to select CH1-CH4 or Ref1-Ref10. When a source channel is selected, the selected channel automatically switches to the ON state.

**TIP**

Besides CH1-CH4 and Ref1-Ref10, the Math2 source can be set to Math1; the Math3 source can be set to Math1 or Math2; the Math4 source can be set to Math1, Math2, or Math3. Selecting a Math automatically enables its window display and sets its Operation on/off switch to ON.

**Scale**

Scale is used to set the vertical scale of the operation result. You can set the vertical scale in the following ways.

• In Math menu, rotate the corresponding multipurpose knob on the front panel or click or tap the icon at the right side of the input field of Scale to increase or decrease the scale value. You can also click or tap the input field to input a specific value with the displayed numeric keypad.

• Close the menu and then adjust the vertical scale with the pinch&stretch gesture on the touch screen. You can also rotate the multipurpose knob 1 on the front panel to adjust the vertical scale. Please refer to Front Panel Overview to configure the front-panel multipurpose knobs.

**Offset**

Offset is used to set the vertical offset of the operation result. You can set the vertical offset in the following ways.

• In Math menu, rotate the corresponding multipurpose knob on the front panel or click or tap the icon at the right side of the input field of Offset to increase or decrease the scale value. You can also click or tap the input field to input a specific value with the displayed numeric keypad.

• Close the menu and then adjust the vertical offset with the drag gesture on the touch screen. You can also rotate the multipurpose knob 2 on the front panel to adjust the vertical offset. Please refer to Front Panel Overview to configure the front-panel multipurpose knobs.

**Invert**

Invert is used to enable or disable the inverted display of the waveform. When the Invert function is disabled, the waveform is displayed normally; when enabled, the voltage values of the displayed waveform are inverted.

**Waveform**

This oscilloscope provides Main and Zoom for the measurement range.
• Main indicates that the measurement range is within the main time base region.

• Zoom indicates that the measurement range is within the zoomed time base region.

To use "Zoom", first enable the Zoom Mode (Delayed Sweep) in the Horizontal System menu.

**Expand**

The oscilloscope supports two vertical expansion modes: GND (default) and Center.

• GND: When the vertical scale is changed, the math operation waveform will expand or compress about the ground level of the signal.

• Center: When the vertical scale is changed, the math operation waveform will expand or compress about the center of the display.

**Auto Set**

Click or tap AutoSetting to adjust the vertical scale and the offset of the operation results to the optimal value according to the current configuration for you to better observe.

**Label**

It is used to set the label for the math operation results. For setting methods, refer to descriptions in To Turn the Channel Label Display On/Off.

**Grid**

For setting methods, refer to the descriptions in To Set the Screen Grid.

## 9.2 Function Operation

In the Math menu, click or tap the Operator drop-down button to select the desired function operation. The available function operation types of this oscilloscope include Intg, Diff, Sqrt, Lg (Base 10 Exponential), Ln, Exp, Abs, and AX+B.

• Intg: calculates the integral of the selected source. For example, you can use integral to measure the area under a waveform or the pulse energy.

• Diff: calculates the discrete time derivative of the selected source. For example, you can use differentiate to measure the instantaneous slope of a waveform.

• Sqrt: calculates the square roots of the selected source point by point and displays the results.

• Lg (Base 10 Exponential): calculates the base 10 exponential of the selected source point by point and displays the results.
• Ln: calculates the natural logarithm (Ln) of the selected source point by point and displays the results.

• Exp: calculates the exponential of the selected source point by point and displays the results.

• Abs: calculates the absolute value of the selected source and displays the results.

• AX+B: applies a linear function to the selected source, and displays the results.

Figure 9.5 Function Operation Menu

**Operation Result Display Window**

Click or tap the Operation on/off switch to enable or disable the display of the operation result window. The source and the vertical scale parameters are displayed at the top of the window, as shown in the figure below.
Figure 9.6 Operation Result Display Window

**Source**

Click or tap the Source drop-down button to select the source from CH1-CH4 or Ref1-Ref10. When a source channel is selected, the selected channel automatically switches to the ON state.

**TIP**

Besides CH1-CH4 and Ref1-Ref10, the Math2 source can be set to Math1; the Math3 source can be set to Math1 or Math2; the Math4 source can be set to Math1, Math2, or Math3. Selecting a Math automatically enables its window display and sets its Operation on/off switch to ON.

**Auto Set**

Click or tap AutoSetting to adjust the vertical scale and the offset of the operation results to the optimal value according to the current configuration for you to better observe.

**Scale**

Scale is used to set the vertical scale of the operation result. You can set the vertical scale in the following ways.

• In Math menu, rotate the corresponding multipurpose knob on the front panel or click or tap the icon at the right side of the input field of Scale to increase or decrease the scale value. You can also click or tap the input field to input a specific value with the displayed numeric keypad.

• Close the menu and then adjust the vertical scale with the pinch&stretch gesture on the touch screen. You can also rotate the multipurpose knob 1 on the front
panel to adjust the vertical scale. Please refer to Front Panel Overview to configure the front-panel multipurpose knobs.

**Offset**

Offset is used to set the vertical offset of the operation result. You can set the vertical offset in the following ways.

• In Math menu, rotate the corresponding multipurpose knob on the front panel or click or tap the icon at the right side of the input field of Offset to increase or decrease the scale value. You can also click or tap the input field to input a specific value with the displayed numeric keypad.

• Close the menu and then adjust the vertical offset with the drag gesture on the touch screen. You can also rotate the multipurpose knob 2 on the front panel to adjust the vertical offset. Please refer to Front Panel Overview to configure the front-panel multipurpose knobs.

**Invert**

Invert is used to enable or disable the inverted display of the waveform. When the Invert function is disabled, the waveform is displayed normally; when enabled, the voltage values of the displayed waveform are inverted.

**Waveform**

This oscilloscope provides Main and Zoom for the measurement range.

• Main indicates that the measurement range is within the main time base region.

• Zoom indicates that the measurement range is within the zoomed time base region.

To use "Zoom", first enable the Zoom Mode (Delayed Sweep) in the Horizontal System menu.

**Label**

It is used to set the label for the math operation results. For setting methods, refer to descriptions in To Turn the Channel Label Display On/Off.

**Expand**

The oscilloscope supports two vertical expansion modes: GND (default) and Center.

• GND: When the vertical scale is changed, the math operation waveform will expand or compress about the ground level of the signal.

• Center: When the vertical scale is changed, the math operation waveform will expand or compress about the center of the display.
**Grid**

For setting methods, refer to the descriptions in To Set the Screen Grid.

**Parameter Setting**

• When the operator is "Intg", click or tap the Offset input field and use the pop-up numeric keypad to set the DC offset calibration factor of the input signal. You can also use the corresponding multipurpose knob to set the value.

• When the operator is "Diff", click or tap Smooth input field and use the pop-up numeric keypad to set the number of smooth times for the differential operation. You can also use the corresponding multipurpose knob to set the value.

• When the operator is "AX+B", click or tap A/B input field and use the pop-up numeric keypad to set the A/B value. You can also use the corresponding multipurpose knob to set the value.

## 9.3 FFT Operation

FFT (Fast Fourier Transform) is used to transform time-domain signals to frequency-domain components (frequency spectrum). This oscilloscope provides FFT operation function which enables you to observe the time-domain waveform and spectrum of the signal at the same time. FFT operation can facilitate the following works:

• Measure harmonic components and distortion in the system;
• Display the characteristics of the noise in DC power;
• Analyze vibration.

In the Math menu, click or tap the Operator drop-down button to select FFT to access the menu as shown in Figure 9.7.
Figure 9.7 FFT Operation Menu

**Operation On/Off**

Click or tap the Operation on/off switch to enable the FFT operation result window. The parameters such as center frequency, frequency range, and resolution are displayed at the top of the window, as shown in the figure below. FFT resolution is the quotient of the sample rate and the number of FFT points. If the number of FFT points is a fixed value, then the higher the sample rate, the higher the resolution.

**NOTE**

The number of FFT analysis points can be 1 Mpts in maximum.

Figure 9.8 FFT Operation Window
**Source**

Click or tap the Source drop-down button to select CH1, CH2, CH3, or CH4 as the source. When a source channel is selected, the selected channel automatically switches to the ON state.

**Auto Set**

Click or tap AutoSetting to adjust the vertical scale and the offset of the operation results to the optimal value according to the current configuration for you to better observe.

**Frequency Range**

In X, select "Span-Center" or "Start-End" mode and then configure the frequency range setting.

• **Span-Center (frequency span to center frequency):** Span specifies the frequency range represented by the width from the frequency at the left side of the window to the frequency at the right side of the window. Divide the frequency span by 10 to obtain the frequency per division.

Click or tap the Center input field to set the frequency of the frequency-domain waveform relative to the horizontal center of the screen. You can also use the corresponding multipurpose knob to set the value. Its range is from 5 Hz to 625 MHz. Click or tap the Span input field to set the frequency span with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. Its range is from 10 Hz to 625 MHz.

• **Start-End (start frequency to stop frequency):** Start frequency specifies the frequency at the left side of the window. Click or tap the Start input field to set the start frequency with the pop-up numeric keypad or use the corresponding multipurpose knob to set the value. Its range is from 0 Hz to (stop frequency-10 Hz). Stop frequency specifies the frequency at the right side of the window. Click or tap the End input field to set the stop frequency with the pop-up numeric keypad or use the corresponding multipurpose knob to set the value. Its range is from (start frequency + 10 Hz) to 625 MHz. By default, it is 10 MHz.

**Vertical Scale/Offset**

In Unit item, you can select dBm/dBV or Vrms as the unit for Scale and Offset.

For how to set the Scale, refer to the descriptions in Scale of "Arithmetic Operation". For how to set the Offset, refer to the descriptions in Offset of "Arithmetic Operation".

**Window Function**

Spectral leakage can be considerably minimized when a window function is used. The oscilloscope provides 6 FFT window functions which have different characteristics and are applicable to measure different waveforms, as shown in the table below. You need to select the window function according to the characteristics of the waveform to be
measured. Click or tap the Window drop-down button to select the desired window function.

Table 9.1 Window Function

| Window Function | Characteristics | Waveforms Applicable to the Window Function |
|-----------------|-----------------|---------------------------------------------|
| Rectangular | Best frequency resolution<br>Poorest amplitude resolution<br>Similar to the situation when no window is applied | Transient or short pulse, the signal levels before and after the multiplication are basically the same<br>Sine waveforms with the same amplitudes and rather similar frequencies<br>Wide band random noise with relatively slow change of waveform spectrum |
| Blackman-Harris | Best amplitude resolution<br>Poorest frequency resolution | Single frequency signal, searching for higher order harmonics |
| Hanning | Better frequency resolution and poorer amplitude resolution compared with Rectangular | Sine, periodic, and narrow band random noise |
| Hamming | A little bit better frequency resolution than Hanning | Transient or short pulse, the signal levels before and after the multiplication are rather different |
| Flattop | Measure the signals accurately | Measure the signal that has no accurate reference and requires an accurate measurement |
| Triangle | Better frequency resolution | Measure the narrow band signal and that has strong noise interference |

**Color Grade**

Click or tap the Color Grade on/off switch to enable/disable the color grade display of FFT operation results. When it is enabled, different colors are displayed on the screen to indicate the times of data acquisition or acquisition probability. Click or tap the Reset button for the Color Grade menu to clear the color grade display and display the color grade again.
**Label**

It is used to set the label for the math operation results. For setting methods, refer to descriptions in To Turn the Channel Label Display On/Off.

**Grid**

For setting methods, refer to the descriptions in To Set the Screen Grid.

**Peak Search**

Click or tap the icon at the right side of Peak Search to enter the peak search menu, as shown in the figure below.

Figure 9.9 Peak Search

• **Peak Search ON/OFF**: click or tap the Peak Search on/off switch to enable or disable the display of the peak search window. By default, it is OFF.

• **Peak Number**: click or tap the input field for the Peak Number menu item and use the pop-up numeric keypad to set the number of peaks. You can also use the corresponding multipurpose knob to set the value. Its range is from 1 to 15. Its default value is 5.

• **Threshold**: click or tap the input field for the Threshold menu item to set the threshold of the peak with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. The range of the threshold is related to the current FFT scale and offset.

• **Excursion**: click or tap the Excursion input field to set the excursion of the peak or use the corresponding multipurpose knob to set the value. The minimum value of Excursion is 0 and its unit is consistent with that of FFT.
• **Table Order**: in Table Order, select Amp Order or Freq Order as the sorting mode. By default, it is "Amp Order".

Click or tap Export, then the save setting interface is displayed. You can export the peak search results to the internal memory or the external USB storage device in CSV format. In the menu, click or tap File Name input field to set the file name; click or tap File Path input field and the disk management menu (Disk Management) is displayed. Select the desired location to save the file and then click or tap Save to save the peak search results.

Clicking or tapping the icon at the right side of Peak Search can close the peak search menu.

## 9.4 Logic Operation

In the Math menu, click or tap the Operator drop-down button to select the desired math operation. The logic operations supported by this oscilloscope include A&&B, A||B, A^B, and !A. After selecting the desired logic operation in the drop-down button of Operator, you can configure its settings for the selected logic operation type.

Figure 9.10 Logic Operation Menu

• **A&&B**: Performs logic "AND" operation on the waveform voltage values of the specified sources point by point and displays the results. In operation, when the voltage value of the source channel is greater than the threshold of the corresponding channel, it is regarded as logic "1"; otherwise it is logic "0". The results of logic AND operation of two binary bits are shown in Table 9.2 Logic Operation.
• **A||B**: Performs logic "OR" operation on the waveform voltage values of the specified sources point by point and displays the results. In operation, when the voltage value of the source channel is greater than the threshold of the corresponding channel, it is regarded as logic "1"; otherwise it is logic "0". The results of logic OR operation of two binary bits are shown in Table 9.2 Logic Operation.

• **A^B**: Performs logic "XOR" operation on the waveform voltage values of the specified sources point by point and displays the results. In operation, when the voltage value of the source channel is greater than the threshold of the corresponding channel, it is regarded as logic "1"; otherwise it is logic "0". The results of logic XOR operation of two binary bits are shown in Table 9.2 Logic Operation.

• **!A**: Performs logic "NOT" operation on the waveform voltage values of the specified sources point by point and displays the results. In operation, when the voltage value of the source channel is greater than the threshold of the corresponding channel, it is regarded as logic "1"; otherwise it is logic "0". The results of logic "NOT" operation of one binary bit are shown in Table 9.2 Logic Operation.

Table 9.2 Logic Operation

| A | B | A&&B | A\|\|B | A^B | !A |
|---|---|------|--------|-----|-----|
| 0 | 0 | 0    | 0      | 0   | 1   |
| 0 | 1 | 0    | 1      | 1   | 1   |
| 1 | 0 | 0    | 1      | 1   | 0   |
| 1 | 1 | 1    | 1      | 0   | 0   |

**Operation Result Display Window**

Click or tap the Operation on/off switch to enable the display of the operation result window. The source and the waveform sizes parameters are displayed at the top of the window, as shown in the figure below.
Figure 9.11 Operation Result Display Window

**Source**

Click or tap the drop-down button of SourceA or SourceB to select CH1, CH2, CH3, or CH4. When a source channel is selected, the selected channel automatically switches to the ON state.

**Waveform Size**

You can select "Small", "Medium", or "Large" as the the waveform display mode.

**Offset**

Offset is used to set the vertical offset of the operation result. You can set the vertical offset in the following ways.

• In Math menu, rotate the corresponding multipurpose knob on the front panel or click or tap the icon at the right side of the input field of Offset to increase or decrease the scale value. You can also click or tap the input field to input a specific value with the displayed numeric keypad.

• Close the menu and then adjust the vertical offset with the drag gesture on the touch screen. You can also rotate the multipurpose knob 2 on the front panel to adjust the vertical offset. Please refer to Front Panel Overview to configure the front-panel multipurpose knobs.
**Sensitivity**

Sets the sensitivity of the digital signal converted from the analog signal on the source. Click or tap the Sensitivity input field to set the sensitivity with the pop-up numeric keypad or use the corresponding multipurpose knob to set the value. For details, refer to Parameter Setting Method.

**Waveform**

This oscilloscope provides Main and Zoom for the measurement range.

• Main indicates that the measurement range is within the main time base region.

• Zoom indicates that the measurement range is within the zoomed time base region.

To use "Zoom", first enable the Zoom Mode (Delayed Sweep) in the Horizontal System menu.

**Threshold**

Click or tap the threshold input field of the specified channel and use the pop-up numeric keypad to set the threshold or use the corresponding multipurpose knob to set the value.

| Thre.CH1 | 0.00V | Thre.CH2 | 0.00V |
|----------|-------|----------|-------|
| Thre.CH3 | 0.00V | Thre.CH4 | 0.00V |

**Label**

It is used to set the label for the math operation results. For setting methods, refer to descriptions in To Turn the Channel Label Display On/Off.

**Grid**

For setting methods, refer to the descriptions in To Set the Screen Grid.

## 9.5 Digital Filter

In the Math menu, click or tap the Operator drop-down button to select the desired math operation. The digital filters supported by this oscilloscope include: low-pass filter, high-pass filter, band-pass filter, and band-stop filter.

• LowPass only allows the signals whose frequencies are lower than the current upper limit frequency to pass.
• HighPass only allows the signals whose frequencies are higher than the current lower limit frequency to pass.

• BandPass only allows the signals whose frequencies are higher than the current lower limit frequency and lower than the current upper limit frequency to pass.

• BandStop only allows the signals whose frequencies are lower than the current lower limit frequency or higher than the current upper limit frequency to pass.

Figure 9.12 Digital Filter Menu

**Operation Result Display Window**

Click or tap the Operation on/off switch to enable the display of the operation result window. The source and the vertical scale parameters are displayed at the top of the window as shown in the figure below.
Figure 9.13 Operation Result Display Window

**Source**

Click or tap the Source drop-down button to select from CH1-CH4 or Ref1-Ref10. When a source channel is selected, the selected channel automatically switches to the ON state.

**TIP**

Besides CH1-CH4 and Ref1-Ref10, the Math2 source can be set to Math1; the Math3 source can be set to Math1 or Math2; the Math4 source can be set to Math1, Math2, or Math3. Selecting a Math automatically enables its window display and sets its Operation on/off switch to ON.

**Auto Set**

Click or tap AutoSetting to adjust the vertical scale and the offset of the operation results to the optimal value according to the current configuration for you to better observe.

**Scale**

Scale is used to set the vertical scale of the operation result. You can set the vertical scale in the following ways.

• In Math menu, rotate the corresponding multipurpose knob on the front panel or click or tap the icon at the right side of the input field of Scale to increase or decrease the scale value. You can also click or tap the input field to input a specific value with the displayed numeric keypad.

• Close the menu and then adjust the vertical scale with the pinch&stretch gesture on the touch screen. You can also rotate the multipurpose knob 1 on the front
panel to adjust the vertical scale. Please refer to Front Panel Overview to configure the front-panel multipurpose knobs.

**Offset**

Offset is used to set the vertical offset of the operation result. You can set the vertical offset in the following ways.

• In Math menu, rotate the corresponding multipurpose knob on the front panel or click or tap the icon at the right side of the input field of Offset to increase or decrease the scale value. You can also click or tap the input field to input a specific value with the displayed numeric keypad.

• Close the menu and then adjust the vertical offset with the drag gesture on the touch screen. You can also rotate the multipurpose knob 2 on the front panel to adjust the vertical offset. Please refer to Front Panel Overview to configure the front-panel multipurpose knobs.

**Invert**

Invert is used to enable or disable the inverted display of the waveform. When the Invert function is disabled, the waveform is displayed normally; when enabled, the voltage values of the displayed waveform are inverted.

**Waveform**

This oscilloscope provides Main and Zoom for the measurement range.

• Main indicates that the measurement range is within the main time base region.

• Zoom indicates that the measurement range is within the zoomed time base region.

To use "Zoom", first enable the Zoom Mode (Delayed Sweep) in the Horizontal System menu.

**Frequency Limit**

• LowPass: click or tap the ωc input field and use the pop-up numeric keypad to set the upper limit frequency or use the corresponding multipurpose knob to set the value.

• HighPass: click or tap the ωc input field and use the pop-up numeric keypad to set the lower limit frequency or use the corresponding multipurpose knob to set the value.

• BandPass: click or tap the ωc1 input field and use the pop-up numeric keypad to set the lower limit frequency. Click or tap the ωc2 input field and use the pop-up numeric keypad to set the upper limit frequency. You can also use the corresponding multipurpose knob to set the lower/upper limit frequency.
• BandStop: click or tap the ωc1 input field and use the pop-up numeric keypad to set the lower limit frequency. Click or tap the ωc2 input field and use the pop-up numeric keypad to set the upper limit frequency. You can also use the corresponding multipurpose knob to set the lower/upper limit frequency.

The settable ranges of the upper and lower limit frequencies are related to the Math sample rate (displayed at the bottom of the screen when the Math function is enabled). The sample rate of the analog channel or the changes of the memory depth can affect the Math sample rate.

**Label**

It is used to set the label for the math operation results. For setting methods, refer to descriptions in To Turn the Channel Label Display On/Off.

**Expand**

The oscilloscope supports two vertical expansion modes: GND (default) and Center.

• GND: When the vertical scale is changed, the math operation waveform will expand or compress about the ground level of the signal.

• Center: When the vertical scale is changed, the math operation waveform will expand or compress about the center of the display.

**Grid**

For setting methods, refer to the descriptions in To Set the Screen Grid.

# 10 Measurements

This series oscilloscope provides the quick measurements after "Auto" is selected, auto measurements for 41 waveform parameters, as well as the cursor measurement function.

## 10.1 Auto Scale

When the oscilloscope is correctly connected and has detected a valid input signal, click or tap the function navigation icon > Auto or press the front-panel key to enable the waveform auto setting function and open the auto setting function menu.

• Click or tap the first icon, and then two periods of the signal are automatically displayed on the screen. Meanwhile, the system will make measurements for the "period" and "frequency" of the currently displayed waveform. The measurement results are displayed in the "Result" bar at the right side of the screen.

• Click or tap the second icon, and then multiple periods of the signal are automatically displayed on the screen. Meanwhile, the system will make measurements for the "period" and "frequency" of the currently displayed waveforms in multiple periods. The measurement results are displayed in the "Result" bar at the right side of the screen.

• Click or tap the third icon to enable the "rise time" measurement item. The measurement results are displayed in the "Result" bar at the right side of the screen. By default, it is intended for the fast edge signal.

• Click or tap the fourth icon to enable the "fall time" measurement item. The measurement results are displayed in the "Result" bar at the right side of the screen. By default, it is intended for the fast edge signal.

• Click or tap the fifth icon to cancel the auto setting and recovers to the parameter settings prior to clicking or tapping Auto.

• Click or tap the sixth icon to enter the Auto Config sub-menu under the Utility menu. For details, please refer to Auto Config.

**TIP**

The waveform auto setting function requires that the frequency of the signal should be greater than or equal to 35 Hz, and the amplitude greater than or equal to 10 mV. If those conditions are not met, the waveform auto setting function may be invalid.
## 10.2 Auto Measurements

You can enter the Measure menu in the following ways.

• Click or tap the function navigation icon at the lower-left corner of the screen, and then select Measure to enter the "Measure" menu.

• Press the front-panel **Measure** key to enter the "Measure" menu.

• Click or tap the Measure button on the toolbar to enter the "Measure" menu.

• In Vertical System menu, click or tap the Measure button to enter the "Measure" menu.

### 10.2.1 Measurement Parameter

This oscilloscope allows you to set the measurement source, enable or disable the all measurement function, the statistical function, and etc. You can make quick measurements for many waveform parameters. The measurement results will be displayed in the Result sidebar at the right section of the screen.

**TIP**

If there is no signal input for the current source or the measurement result is not within the valid range (too large or too small), then the measurement results are invalid, and "*****" is displayed on the screen. Please re-input the signal or set the signal.

#### 10.2.1.1 Time Parameters

Figure 10.1 Time Parameters
• **Period**: defined as the time between the middle threshold points of two consecutive, like-polarity edges.

• **Frequency**: defined as the reciprocal of period.

• **Rise Time**: indicates the time for the signal amplitude to rise from the threshold lower limit to the threshold upper limit.

• **Fall Time**: indicates the time for the signal amplitude to rise from the threshold upper limit to the threshold lower limit.

• **+Width**: indicates the time between the threshold middle value of a rising edge to the threshold middle value of the next falling edge.

• **-Width**: indicates the time between the threshold middle value of a falling edge to the threshold middle value of the next rising edge.

• **+Duty**: indicates the ratio of the positive pulse width to the period.

• **-Duty**: indicates the ratio of the negative pulse width to the period.

• **Tvmax**: indicates the time that corresponds to the maximum value of the waveform (Vmax).

• **Tvmin**: indicates the time that corresponds to the minimum value of the waveform (Vmin).

The default values for threshold upper limit, threshold middle value, and threshold lower limit are 90%, 50%, and 10%, respectively.

#### 10.2.1.2 Count Values

The default values for threshold upper limit and threshold lower limit are 90% and 10%, respectively.

**Positive Pulse Count**

It is specified as the number of positive pulses that rise from under the threshold lower limit to above the threshold upper limit.
**Negative Pulse Count**

It is specified as the number of negative pulses that fall from above the threshold upper limit to below the threshold lower limit.

Negative Pulse Count = n

**Rising Edge Count**

It is specified as the number of rising edges that rise from under the threshold lower limit to above the threshold upper limit.

Rising Edge Count = n

**Falling Edge Count**

It is specified as the number of falling edges that fall from above the threshold upper limit to below the threshold lower limit.
Falling Edge Count = n

#### 10.2.1.3 Delay and Phase Parameters

Figure 10.2 Delay and Phase Parameters

1. **Delay(r-r)**: indicates the time difference between the threshold middle values of the rising edge of Source A and that of Source B. Negative delay indicates that the rising edge of Source A occurred after that of Source B.

2. **Delay(f-f)**: indicates the time difference between the threshold middle values of the falling edge of Source A and that of Source B. Negative delay indicates that the falling edge of Source A occurred after that of Source B.

3. **Delay(r-f)**: indicates the time difference between the threshold middle values of the rising edge of Source A and the falling edge of Source B. Negative delay indicates that the rising edge of Source A occurred after the falling edge of Source B.

4. **Delay(f-r)**: indicates the time difference between the threshold middle values of the falling edge of Source A and the rising edge of Source B. Negative delay indicates that the falling edge of Source A occurred after the rising edge of Source B.

5. **Phase(r-r)**: indicates the phase deviation between the threshold middle values of the rising edge of Source A and that of Source B. The phase formula is as follows:
PhaseA_RBR = (DelayA_RBR / Period_sourceA) × 360°

Wherein, PhaseARBR represents Phase(r-r), DelayARBR represents Delay(r-r), and PeriodsourceA represents the period of Source A.

6. **Phase(f-f)**: indicates the phase deviation between the threshold middle values of the falling edge of Source A and that of Source B. The phase formula is as follows:

PhaseA_FBF = (DelayA_FBF / Period_sourceA) × 360°

Wherein, PhaseAFBF represents Phase(f-f), DelayAFBF represents Delay(f-f), and PeriodsourceA represents the period of Source A.

7. **Phase(r-f)**: indicates the phase deviation between the threshold middle values of the rising edge of Source A and the falling edge of Source B. The phase formula is as follows:

PhaseA_RBF = (DelayA_RBF / Period_sourceA) × 360°

Wherein, PhaseARBF represents Phase(r-f), DelayARBF represents Delay(r-f), and PeriodsourceA represents the period of Source A.

8. **Phase(f-r)**: indicates the phase deviation between the threshold middle values of the falling edge of Source A and the rising edge of Source B. The phase formula is as follows:

PhaseA_FBR = (DelayA_FBR / Period_sourceA) × 360°

Wherein, PhaseAFBR represents Phase(f-r), DelayAFBR represents Delay(f-r), and PeriodsourceA represents the period of Source A.

**TIP**

• Source A and Source B can be any channel among CH1-CH4 and Math1-Math4.

• The default threshold middle value is 50%.
#### 10.2.1.4 Voltage Parameters

Figure 10.3 Voltage Parameters

1. **Vmax**: indicates the voltage value from the highest point of the waveform to the GND.

2. **Vmin**: indicates the voltage value from the lowest point of the waveform to the GND.

3. **Vpp**: indicates the voltage value from the highest point to the lowest point of the waveform.

4. **Vtop**: indicates the voltage value from the flat top of the waveform to the GND.

5. **Vbase**: indicates the voltage value from the flat base of the waveform to the GND.

6. **Vamp**: indicates the voltage value from the top of the waveform to the base of the waveform.

7. **Vupper**: indicates the actual voltage value that corresponds to the threshold maximum value.

8. **Vmid**: indicates the actual voltage value that corresponds to the threshold middle value.

9. **Vlower**: indicates the actual voltage value that corresponds to the threshold minimum value.

10. **Vavg**: indicates the arithmetic average value on the whole waveform or in the gating area. The formula is shown as follows:

Average = Σ(i=1 to n) xi / n
Wherein, xi is the ith point, and n is the number of points being measured.

11. **VRMS**: indicates the root mean square value on the whole waveform or in the gating area. The formula is as follows:

RMS = √(Σ(i=1 to n) xi²/n)

Wherein, xi is the measurement result of the ith point, and n is the number of points being measured.

12. **Per.VRMS**: indicates the root mean square value within a period. The formula is as shown above.

13. **Overshoot**: indicates the ratio of the difference between the maximum value and the top value of the waveform to the amplitude value.

14. **Preshoot**: indicates the ratio of the difference between the minimum value and the base value of the waveform to the amplitude value.

15. **AC RMS**: indicates the root-mean-square value of the waveforms, with the DC component removed. The formula is shown as follows:

Std.Dev = √(Σ(i=1 to n) (xi - Average)²/n)

Wherein, xi is the amplitude of the ith point, Average is the waveform average value, and n is the number of points being measured.

#### 10.2.1.5 Other Parameters

• **Positive Slew Rate**: On the rising edge, first calculate the difference between the high value and the low value, then use the difference to divide the corresponding time value to obtain the positive slew rate.

• **Negative Slew Rate**: On the falling edge, first calculate the difference between the low value and the high value, then use the difference to divide the corresponding time value to obtain the negative slew rate.

• **Area**: indicates the area of the whole waveform within the screen. The unit is V*s. The area of the waveform above the zero reference (namely the vertical offset) is positive, and the area of the waveform below the zero reference is negative. The area measured is the algebraic sum of the area of the whole waveform within the screen.

• **Period Area**: indicates the area of the first period of waveform on the screen. The unit is V*s. The area of the waveform above the zero reference (namely the vertical offset) is positive, and the area of the waveform below the zero
reference is negative. The area measured is the algebraic sum of the whole period area.

### 10.2.2 Select the Measurement Item

In the Measure menu, click or tap Horizontal, Vertical, or Other to go to the desired menu. You can also slide to select the measurement item to enter the corresponding interface, as shown in Figure 10.4, Figure 10.5, and Figure 10.6. Click or tap any of the measurement items to enable the measurements. This series allows you to enable measurements of up to 14 items at the same time.

**TIP**

You can also refer to Multi-pane Windowing to enable all measurements.

• Vertical: Vmax, Vmin, Vpp, Vtop, Vbase, Vamp, Vupper, Vmid, Vlower, Vavg, VRMS, Per. VRMS, Overshoot, Preshoot, Area, Per.Area, and AC.RMS.

Figure 10.4 Vertical Measurement Items

• Horizontal: Period, Frequency, Rise Time, Fall Time, +Width, -Width, +Duty, -Duty, Positive Pulse Count, Negative Pulse Count, Rising Edge Count, Falling Edge Count, Tvmax, Tvmin, +Slew Rate, and -Slew Rate.
Figure 10.5 Horizontal Measurement Items

• Other: Delay(r-r), Delay(r-f), Delay(f-r), Delay(f-f), Phase(r-r), Phase(r-f), Phase(f-r), and Phase(f-f).

Figure 10.6 Other Measurement Items
### 10.2.3 Measurement Settings

In the Measure menu, click or tap the Setting button to enter the measurement setting menu.

Figure 10.7 Measurement Settings Menu

**Histogram**

Click or tap the Histogram on/off switch to enable or disable the histogram function. After the histogram function is enabled, the Measure Histogram view is displayed on the screen, as shown in the figure below. The histogram analysis result label is displayed in the Result sidebar (refer to Histogram Analysis Results).

**NOTE**

Add at least one measurement item (Select the Measurement Item) before enabling the Measure Histogram function.
After the Measure Histogram function is enabled, please refer to Select the Measurement Item to add new measurement parameter. The new parameter will be used as the measurement item. In the "Result" sidebar, you can also click or tap the label of the added measurement parameter (e.g. "Vpp" and "Vmin") to change the measurement item.

**Indicator**

Click or tap the Indicator on/off switch to enable or disable the indicator.

If enabled, one or more cursors will be displayed on the screen. Before enabling the indicator, you need to enable at least one auto measurement parameter and the number of cursors will change with the measurement parameter enabled.

**TIP**

When no measurement parameter is selected or there is no source input, the indicator is not available. The indicator changes when the waveform is expanded or compressed horizontally.

**Measurement Threshold**

• First, select % or Abs as the display type.

• Click or tap the drop-down button of Source to select the desired channel. You can select from CH1-CH4 or Math1-Math4.

• Click or tap the input field of Upper and use the pop-up numeric keypad to set the upper limit of the measurement or use the corresponding multipurpose knob to set the value. When the upper limit is set to be smaller than or equal to the current middle value, a prompt message "Set at lower limit" is displayed. Then, the oscilloscope will automatically adjust the upper limit and make it greater than the middle value. By default, it is 90%. The default absolute value varies with the vertical setting of the channel.

• Click or tap the input field of Mid and use the pop-up numeric keypad to set the middle value of the measurement or use the corresponding multipurpose knob to set the value. The middle value is limited by the settings of the upper limit and lower limit. By default, it is 50%. The default absolute value varies with the vertical setting of the channel.

• Click or tap the input field of Lower and use the pop-up numeric keypad to set the lower limit of the measurement or use the corresponding multipurpose knob to set the value. When the lower limit is set to be greater than or equal to the current middle value, a prompt message "Set at upper limit" is displayed. Then, the oscilloscope will automatically adjust the lower limit and make it smaller than the middle value. By default, it is 10%. The default absolute value varies with the vertical setting of the channel.

• Click or tap Default to return the upper, middle, and lower limits to their default values.
Click or tap the Threshold on/off switch to enable or disable the threshold settings.

**TIP**

Modifying the threshold will affect the measurement results of time, delay, and phase parameters.

**Measurement Range**

Click or tap the drop-down button of the Region to select "Main" or "Zoom".

• Main: indicates that the measurement range is within the main time base region.

• Zoom: indicates that the measurement range is within the zoomed time base region.

**TIP**

To use "Zoom", you need to enable the Zoom Mode (Delayed Sweep) first.

**Amplitude Measurement Method**

Click or tap Auto or Manual as the amplitude measurement method, which affects the measurement method for the top and base values

If you select "Manual", set the following parameters:

• Click or tap the Top toggle button to select Histogram or Max-Min as the top value measurement method.

• Click or tap the Base toggle button to select Histogram or Max-Min as the base value measurement method.

**TIP**

If you select "Manual" for the amplitude method, the measurement results of other parameters may be affected.

"Histogram" and "Max-Min" are the internal measurement algorithm for the oscilloscope. The "Histogram" method mentioned above is different from the Histogram function of the oscilloscope.

**Remove the Measurement Results**

Refer to Remove the Measurement Results.
**Statistics**

Click or tap the Statistic on/off switch to enable or disable the statistical result display. You can also click or tap at the lower-right of the measurement item in the "Result" sidebar to expand the label to display all the statistical items. Click or tap to collapse the label. The figure below shows the displayed results after the Statistic of period measurement is enabled.

• Click or tap any measurement item in the "Result" sidebar at the right side of the screen and a window is displayed. Click or tap Reset Stat. to clear the history statistics data and makes statistics again. You can also click or tap Reset Stat. in the measurement setting menu.

• Click or tap the input field of Count and use the pop-up numeric keypad to set the count value. You can also use the corresponding multipurpose knob to set the value. Its range is from 2 to 100000. Its default value is 1000.

### 10.2.4 Remove the Measurement Results

This oscilloscope allows you to delete the measurement results of the parameters.

• In Measure setting menu, click or tap Remove to delete the currently selected measurement item that you've added; click or tap Remove All to delete all the displayed measurement items.

• Click or tap any measurement item in the "Result" sidebar at the right side of the screen and a window is displayed. Click or tap Remove to delete the currently
selected measurement item that you've added; click or tap **Remove All** to delete all the displayed measurement items.

• In the "Result" sidebar, select a measurement item and drag it to the right to delete it quickly

## 10.3 Cursor Measurements

Cursor measurement can measure the X axis values (e.g. Time) and Y axis values (e.g. Voltage) of the selected waveform. Before making cursor measurements, connect the signal to the oscilloscope to acquire stable display. The cursor measurement function provides the following two cursors.

Figure 10.8 Cursors

• **X Cursor**

X cursor is a vertical solid/dotted line that is used to make horizontal adjustments. It can be used to measure time (s) and frequency (Hz).

- Cursor A is a vertical solid line (**AX** is displayed at the bottom of the screen), and Cursor B is a vertical dotted line (**BX** is displayed at the bottom of the screen).

- In the XY cursor mode, X cursor is used to measure the waveform amplitude of Source X.

• **Y Cursor**

Y cursor is a horizontal solid/dotted line that is used to make vertical adjustments. It can be used to measure amplitude (the unit is the same as that of the source channel amplitude).
- Cursor A is a horizontal solid line (AY is displayed at the right section of the screen), and Cursor B is a horizontal dotted line (BY is displayed at the right section of the screen).

- In XY cursor mode, Y cursor is used to measure the waveform amplitude of Source Y.

You can enable cursor measurements in the following ways.

• Click or tap the function navigation icon > Cursors to enable cursor measurements.

• Click or tap the Cursors button on the toolbar to enable cursor measurements.

• Press the front-panel Cursor key to enable cursor measurements.

The measurement results are displayed in the "Result" bar at the right side of the screen.

• AX: indicates the X value at Cursor A.

• AY: indicates the Y value at Cursor A.

• BX: indicates the X value at Cursor B.

• BY: indicates the Y value at Cursor B.

• ∆X: indicates the horizontal spacing between Cursor A and Cursor B.

• ∆Y: indicates the vertical spacing between Cursor A and Cursor B.
• 1/∆X: indicates the reciprocal of the horizontal spacing between Cursor A and Cursor B.

Click or tap the result bar and then select Remove or Setting in the pop-up window.

• Click or tap Remove. Then the current cursor measurement results will be cleared.

• Click or tap Setting. Then the "Cursors" menu is displayed. You can select the cursor mode: Manual, Track, and XY.

### 10.3.1 Manual Mode

In the manual cursor mode, you can adjust the cursor manually to measure the value of the waveforms of the specified source at the current cursor. If the settings for the parameter such as the cursor type and measurement source are different, the measurement results will be different for cursor measurement.

In the Cursors menu, click or tap Manual for the Mode item to enable the Manual cursor measurement function. The measurement results are displayed in the "Result" bar at the right side of the screen. When you change the cursor position, the measurement results will be changed accordingly.

Figure 10.9 Manual Mode Setting Menu

**Select the Measurement Source**

Click or tap the drop-down button of Source to select the desired channel (None, CH1-CH4, or Math1-Math4).

When a specified channel is selected as the source, it will be automatically turned on.

**Select Cursor Type**

Click or tap the Select toggle button to select "X" or "Y".
• **X**: It is a pair of vertical solid (Cursor A)/dotted (Cursor B) lines, used for measuring time parameters. The measurement results include AX, BX, ∆X, and 1/∆X.

• **Y**: It is a pair of horizontal solid (Cursor A)/dotted (Cursor B) lines, used for measuring voltage parameters. The measurement results include AY, BY, and ∆Y.

**Adjust Cursor Position**

1. When "X" is selected, you can adjust the position of X cursor.

- Click or tap the input field of AX and use the pop-up numeric keypad to set the horizontal position of Cursor A (X cursors). The horizontal axis indicates time, and the unit of its setting value is the same as that of the horizontal unit. Its adjustable range is limited within the screen.

- Click or tap the input field of BX and use the pop-up numeric keypad to set the horizontal position of Cursor B (X cursors). The horizontal axis indicates time, and the unit of its setting value is the same as that of the horizontal unit. Its adjustable range is limited within the screen.

- Click or tap the AX BX on/off switch to turn on/off adjusting the horizontal position of Cursor A and Cursor B (X cursors) simultaneously. The horizontal spacing between Cursor A and Cursor B (X cursors) remains unchanged.

2. When "Y" is selected, you can adjust the position of Y cursor.

- Click or tap the input field of AY, and then use the pop-up numeric keypad to set the vertical position of Cursor A (Y cursors). The vertical axis indicates voltage, and the unit of its setting value is the same as that of the vertical unit.

- Click or tap the input field of BY and use the pop-up numeric keypad to set the vertical position of Cursor B (Y cursor). The vertical axis indicates voltage, and the unit of its setting value is the same as that of the vertical unit.

- Click or tap the AY BY on/off switch to turn on/off adjusting the vertical position of Cursor A and Cursor B (Y cursors) simultaneously. The vertical spacing between Cursor A and Cursor B (Y cursors) remains unchanged.

You can also use the front-panel multipurpose knob to adjust the cursor position. To configure the multipurpose knobs, please refer to Front Panel Overview.

**Measurement Example**

Measure the period of a sine wave by using the manual cursor measurement and auto measurement respectively. The measurement results are both 200 ns.
Figure 10.10 Manual Cursor Measurement Example

**Disable the Cursor Measurement Function**

When cursor measurement is enabled, you can disable it in the following ways:

• In the Cursors menu, click or tap the **Remove** button to disable cursor measurements.

• In the "Result" bar at the right side of the screen, click or tap the "Cursors" label and then click or tap **Remove** in the pop-up window.

• In the "Result" bar at the right side of the screen, drag the "Cursors" label to the right to simply disable cursor measurements.

• Press the front-panel **Cursor** key to disable cursor measurements.

### 10.3.2 Track Mode

In the Track mode, you can adjust the two pairs of cursors (Cursor A and Cursor B) to measure the X and Y values on two different sources respectively. When the cursors are moved horizontally/vertically, the markers will position on the waveform automatically. When the waveform is expanded or compressed horizontally/vertically, the markers will track the points being marked at the last adjustment of the cursors.

In the Cursors menu, click or tap **Track** for the Mode item to enable the Track cursor measurement function. The measurement results are displayed in the "Result" bar at the right section of the screen.
Figure 10.11 Track Mode Setting Menu

**Select the Measurement Source**

• Click or tap the drop-down button of AX Source to select the desired channel (None, CH1-CH4, or Math1-Math4).

• Click or tap the drop-down button of BX Source to select the desired channel (None, CH1-CH4, or Math1-Math4).

When a specified channel is selected as the source, it will be automatically turned on.

**Select the Track Mode**

Click or tap the Track toggle button to select "X" or "Y" as the current track axis. By default, it is "X".

• X: When the X cursor position is adjusted, Y cursor will automatically track the intersection point between X cursor and source signal

• Y: When the Y cursor position is adjusted, X cursor will automatically track the intersection point between Y cursor and source signal.

**Adjust Cursor Position**

• When "X" is selected, you can adjust the position of X cursor.

- Click or tap the input field of AX and use the pop-up numeric keypad to set the horizontal position of Cursor A (X cursors). Its adjustable range is limited within the screen.

- Click or tap the input field of BX and use the pop-up numeric keypad to set the horizontal position of Cursor B (X cursors). Its adjustable range is limited within the screen.
- Click or tap the AX BX on/off switch to turn on/off adjusting the horizontal position of Cursor A and Cursor B (X cursors) simultaneously. The horizontal spacing between Cursor A and Cursor B (X cursors) remains unchanged.

• When "Y" is selected, you can adjust the position of Y cursor.

- Click or tap the input field of AY, and then use the pop-up numeric keypad to set the vertical position of Cursor A (Y cursors).

- Click or tap the input field of BY and use the pop-up numeric keypad to set the vertical position of Cursor B (Y cursor).

- Click or tap the AY BY on/off switch to turn on/off adjusting the vertical position of Cursor A and Cursor B (Y cursors) simultaneously. The vertical spacing between Cursor A and Cursor B (Y cursors) remains unchanged.

You can also use the front-panel multipurpose knob to adjust the cursor position. To configure the multipurpose knobs, please refer to Front Panel Overview.

**Measurement Example**

Set the AX Source to CH1, BX Source to CH2, and Track to "X".

When the AX cursor position is adjusted, AY cursor will automatically track the intersection point between AX cursor and source signal (CH1); When the BX cursor position is adjusted, BY cursor will automatically track the intersection point between BX cursor and source signal (CH2). The measurement results are displayed in the "Result" bar, as shown in Figure 10.12. Then, expand the waveforms horizontally, and you will find that the cursor will track the point that has been marked, as shown in Figure 10.13.

Figure 10.12 Track Measurement (before Horizontal Expansion)
Figure 10.13 Track Measurement (after Horizontal Expansion)

**Disable the Cursor Measurement Function**

When cursor measurement is enabled, you can disable it in the following ways:

• In the Cursors menu, click or tap the Remove button to disable cursor measurements.

• In the "Result" bar at the right side of the screen, click or tap the "Cursors" label and then click or tap Remove in the pop-up window.

• In the "Result" bar at the right side of the screen, drag the "Cursors" label to the right to simply disable cursor measurements.

• Press the front-panel **Cursor** key to disable cursor measurements.

### 10.3.3 XY Mode

In the Cursors menu, click or tap XY for the Mode item to enable the XY cursor measurement function. The measurement results are displayed in the "Result" bar at the right section of the screen.

Figure 10.14 XY Mode Setting Menu
**TIP**

By default, XY mode is unavailable. It is available only when the horizontal time base mode is "XY". To enable the XY mode, please refer to Enable the XY Mode.

**Adjust Cursor Position**

• Click or tap to select the "X" tab under the Select menu item to set the X value for the specified cursor.

- Click or tap the input field of AX and use the pop-up numeric keypad to set the X value at Cursor A.

- Click or tap the input field of BX and use the pop-up numeric keypad to set the X value at Cursor B.

- Click or tap the AX BX on/off switch to turn on/off adjusting the X value at Cursor A and the X value at Cursor B simultaneously.

• Click or tap to select "Y" under the Select item to set the Y value for the specified cursor.

- Click or tap the input field of AY and use the pop-up numeric keypad to set the Y value at Cursor A.

- Click or tap the input field of BY and use the pop-up numeric keypad to set the Y value at Cursor B.

- Click or tap to the AY BY on/off switch to turn on/off adjusting the Y value at Cursor A and the Y value at Cursor B simultaneously.

You can also use the front-panel multipurpose knob to adjust the cursor position. To configure the multipurpose knobs, please refer to Front Panel Overview. During the adjustment, the measurement results will change accordingly. The adjustable range is limited within the screen.

**Disable the Cursor Measurement Function**

When cursor measurement is enabled, you can disable it in the following ways:

• In the Cursors menu, click or tap the Remove button to disable cursor measurements.

• In the "Result" bar at the right side of the screen, click or tap the "Cursors" label and then click or tap Remove in the pop-up window.

• In the "Result" bar at the right side of the screen, drag the "Cursors" label to the right to simply disable cursor measurements.

• Press the front-panel **Cursor** key to disable cursor measurements.

# 11 Digital Voltmeter (DVM) and Frequency Counter

This series oscilloscope provides a built-in digital voltmeter (DVM) and frequency counter, which enable you to perform more accurate measurements, improving user experience in counter and frequency measurement.

## 11.1 Digital Voltmeter (DVM)

The built-in DVM of this oscilloscope provides 4-digit voltage measurements on any analog channel. DVM measurements are asynchronous from the oscilloscope's acquisition system and are always acquiring. You can enable the DVM measurements in the following ways.

• Click or tap the function navigation icon > DVM to enable DVM measurements.

• Click or tap the DVM button on the toolbar to enable DVM measurements.

• Press the front-panel key and then select DVM in the displayed "Analyse" menu to enable the DVM measurements.

After the DVM measurements are enabled, the "DVM" label appears in the "Result" bar at the right section of the screen, as shown in the figure below.

The voltage value in the label shows the measurement extrema over the last 3 seconds.

Click or tap the "DVM" label and then a window is displayed. Click or tap Setting to enter the DVM setting menu as shown in Figure 11.1. You can click or tap Remove to disable DVM measurements.

### 11.1.1 Measurement Settings

After the DVM is enabled, click or tap the "DVM" label in the "Result" bar at the right section of the screen and a window is displayed. Click or tap Setting in the window to enter the DVM setting menu, as shown in the figure below.
Figure 11.1 DVM Setting Menu

**Select the Measurement Source**

Click or tap the Source drop-down button to select the desired source. The analog channel (CH1-CH4) can be selected to be the measurement source.

Even if the analog channel (CH1-CH4) is not enabled, you can still perform the DVM measurements.

**Select the Measurement Mode**

In the Mode item, you can select the DVM mode. The DVM measurement modes include AC RMS, DC, and AC+DC RMS.

• AC RMS: displays the root-mean-square value of the acquired data, with the DC component removed.

• DC: displays the average value of the acquired data.

• AC+DC RMS: displays the root-mean-square value of the acquired data.

**Set the Limits**

Click or tap the Beeper on/off switch to turn on or off the beeper. When the beeper is turned on, you can enable the beeper to sound an alarm when the voltage value is inside or outside the limited range.

• **Limits Condition Setting**

Click or tap the When toggle button to select "In Limits" or "Out Limits".

- In Limits: when the voltage value is inside the limited range, you can enable or disable the beeper to sound an alarm.
- Out Limits: when the voltage value is outside the limited range, you can enable or disable the beeper to sound an alarm.

• **Upper/Lower Limit Setting**

Click or tap the input field of Upper, then use the pop-up numeric keypad to set the upper limit of the voltage or use the corresponding multipurpose knob to set the value.

Click or tap the input field of Lower, and then use the pop-up numeric keypad to set the lower limit of the voltage or use the corresponding multipurpose knob to set the value.

### 11.1.2 Remove the Measurement

Click or tap the "DVM" label in the "Result" bar and a window is displayed. Click or tap Remove to disable DVM measurements and clear the measurement results. You can also click or tap Remove in the DVM setting menu to disable the function.

## 11.2 Frequency Counter

The frequency counter analysis function provides frequency, period, or edge event counter measurements on any analog channel.

You can enable the counter in the following ways:

• Click or tap > Counter to enable the counter.

• Click or tap the Counter button on the toolbar to enable the counter.

• Press the front-panel key and then select Counter in the displayed "Analyse" menu to enable the counter.

After the counter is enabled, the "Counter" label displaying the counter measurement results appears in the "Result" bar at the right section of the screen, as shown in the figure below. You can set the Statistic switch to "ON" in "Counter" menu to enable the statistical results. You can refer to Statistics Results.
You can click or tap the "Counter" label in the "Result" bar and select Reset Stat., Setting, or Remove in the displayed window.

### 11.2.1 Measurement Settings

After the frequency counter is enabled, click or tap the "Counter" label in the "Result" bar at the right section of the screen and a window is displayed. Click or tap Setting in the window to enter the counter setting menu, as shown in the figure below.

Figure 11.2 Frequency Counter Setting Menu

**Select the Measurement Source**

Click or tap the drop-down button of Source to select the desired source. Analog channels (CH1-CH4) and EXT (for two-channel models only) can be selected as the source of the frequency counter.

**Set Resolution**

For Period and Frequency measurements, you need to set the readout resolution. Click or tap the input field of Resolution to set the resolution by using the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. The range of resolution is from 3 bits to 6 bits. By default, it is 4 bits. The greater the resolution, the longer the gate time. In this way, the measurement time will be longer.

**Select the Measurement Item**

In the Measure item, you can select the desired measurement item. Available options include Frequency, Period, and Totalize. Wherein, Totalize indicates the count of edge events on the signal.
**Clear Count**

When "Totalize" is selected as the measurement item, the oscilloscope measures the count of edge events on the signal. At this time, click or tap Clear Count to clear the measurement results and start the measurements again.

**Statistics Results**

When "Frequency" or "Period" is selected, click or tap the Statistic on/off switch to turn on/off displaying all statistical items. When enabled, all the statistical results will be displayed in the "Counter" label in the "Result" bar.

### 11.2.2 Reset Statistics

Click or tap the "Counter" label in the "Result" bar at the right section of the screen and a window is displayed. Click or tap Reset Stat. in the window to reset the statistics.

### 11.2.3 Remove the Measurement

Click or tap the "Counter" label in the "Result" bar at the right section of the screen and a window is displayed. Click or tap Remove to clear the measurement results. The "Counter" label disappears from the "Result" bar accordingly. You can also click or tap Remove in the counter setting menu to disable the function.

# 12 Histogram Analysis

The histogram analysis function can provide the statistic view for waveform and measurement results, enabling you to judge the trend of waveforms, and quickly locate the potential problems of the signal. This series oscilloscope supports histogram types including Horizontal, Vertical, and Measure. For the Measure Histogram function, refer to Histogram of the "Measurements" chapter. This chapter only introduces the Horizontal and Vertical histogram.

Click or tap the function navigation icon and select Histogram to enter the Histogram menu.

Figure 12.1 Histogram Menu

## 12.1 To Enable or Disable the Histogram Function

In Histogram menu, click or tap the Enable on/off switch to enable or disable the histogram analysis. After the histogram function is enabled, with the on-going acquisition and measurement of the waveforms, the height of the bar graph will change within the set range of the histogram window to indicate the number of times for data statistics.

Take horizontal histogram as an example. After the histogram function is enabled, the histogram analysis view as shown in the figure below is displayed on the screen. Also, the "Histogram" label appears on the Result bar at the right side of the screen.
Figure 12.2 Histogram Analysis Interface

When the histogram function is enabled, you can click or tap the "Histogram" label > Setting to open the histogram setting menu. You can also click or tap the histogram plot area to quickly open the histogram setting menu.

**TIP**

For definitions of the measurement items in the "Histogram" label, refer to Histogram Analysis Results.

## 12.2 To Select the Histogram Type

In the Histogram menu, click or tap the Type drop-down button to select the histogram type.

• Horizontal: displays the number of times for statistics making in the forms of columns in the histogram bar graph at the bottom of the graticule.

• Vertical: displays the number of times for statistics making in the forms of rows in the histogram bar graph at the left of the graticule.

## 12.3 To Select the Histogram Source

In the Histogram menu, Click or tap the Source drop-down button to select the desired source. The analog channels (CH1-CH4) can be selected to be the histogram source.

## 12.4 To Set the Histogram Height

The histogram height indicates the number of grids the histogram bar graph should use on the screen.
In Histogram menu, click or tap the input field of Height, and then use the pop-up numeric keypad to set the height. It ranges from 1 div to 4 div, and the default is 2 div.

## 12.5 To Set the Histogram Range

You need to set the histogram window range. Adjust the size and position of the histogram window by setting the "Left Limit", "Right Limit", "Top Limit", and "Bottom Limit" respectively.

• Click or tap the Left Limit input field and use the pop-up numeric keypad to set the value. You can also use the corresponding multipurpose knob to set the value.

• Click or tap the Right Limit input field and use the pop-up numeric keypad to set the value. You can also use the corresponding multipurpose knob to set the value.

• Click or tap the Top Limit input field and use the pop-up numeric keypad to set the value. You can also use the corresponding multipurpose knob to set the value.

• Click or tap the Bottom Limit input field and use the pop-up numeric keypad to set the value. You can also use the corresponding multipurpose knob to set the value.

**NOTE**

Adjusting the horizontal time base or vertical scale will not affect the histogram limit range, but only shows variation with the scale.

**TIP**

You can also drag the histogram window in white to adjust the window's size and position.

## 12.6 Histogram Analysis Results

After the histogram analysis function is enabled, the "Histogram" label will be displayed in the Result sidebar, as shown in the figure below. Note that when the histogram type is set to Histogram, the statistical data results also include the parameter XScale.
Figure 12.3 Histogram Analysis Results

• **Sum**: indicates the sum of all bins (buckets) in the histogram.

• **Peaks**: indicates the maximum number of hits in any single bin.

• **Max**: indicates the maximum value.

• **Min**: indicates the minimum value.

• **Pk_Pk**: indicates the Delta (Max-Min) between the max. value and the min. value.

• **Mean**: indicates the average value of the histogram.

• **Median**: indicates the median value of the histogram.

• **Mode**: indicates the mode value of the histogram.

• **Bin width**: indicates the width of each bin (bucket) in the histogram.

• **Sigma**: indicates the standard deviation of the histogram.

• **XScale**: indicates the horizontal scale of the histogram. It is 100 times the value of Bin width.
## 12.7 To Remove Results

• Click or tap the "Histogram" label in the Result sidebar and a window is displayed. Click or tap Remove in the window to remove measurement results and disable the histogram function.

• In the "Result" bar at the right side of the screen, drag the "Histogram" label to the right to quickly remove results and disable the histogram function.

## 12.8 To Clear Statistics

Click or tap the "Histogram" label in the Result sidebar and a window is displayed. Click or tap Clear in the window to clear all statistical data and restart to make statistics.

# 13 Reference Waveform

This series oscilloscope provides 10 reference waveform positions (Ref1-Ref10). In the actual test process, you can compare the signal waveform with the reference waveform to locate the failure.

## 13.1 To Enable Ref Function

You can access the Ref menu in the following ways.

• Click or tap the function navigation icon at the lower-left corner of the screen, and then select Ref to enter the reference waveform function menu.

• Press the front-panel key to enter the reference waveform function menu.

Figure 13.1 Reference Waveform Menu

When the Ref function is enabled, you can select different colors for reference waveforms, set the source of each reference channel, adjust the vertical scale and offset of the reference waveform, save the reference waveform to the internal or external memory, and recall it when necessary.

## 13.2 To Set the Reference Waveform

In the Ref menu, you can specify a channel to serve as the reference channel. You can save or clear the reference channel.

**Select the Reference Channel**

Click or tap the drop-down button of Current to select the reference waveform channel (Ref1-Ref10). By default, Ref1 is enabled.
**Select the Ref Source**

Click or tap the drop-down button of Source to select the desired reference waveform source (CH1-CH4 or Math1-Math4).

**Save the Reference Waveform to Internal Memory**

Click or tap SaveToRef to save the displayed waveform for the specified source to the internal memory as the reference waveform.

**CAUTION**

This operation only saves the reference waveform to the volatile memory, and the waveform will be cleared at power-off or restored to the default settings. If you want to store reference waveforms that can be recalled when necessary, please export the waveform to internal or external memory (Export to Internal or External Memory)

**Clear the Specified Reference Waveform**

Click or tap Clear to clear the specified reference waveform for the "current channel".

You can also click or tap the Clear button in the function navigation menu or press the front-panel key to clear the reference waveforms of all the reference channels.

## 13.3 To Set the Ref Waveform Display

After clicking or tapping SaveToRef, you can adjust the vertical scale and offset of the reference waveform specified in Current.

**Modify the Vertical Scale**

Click or tap the input field of VScale, and then use the pop-up numeric keypad to set the vertical scale of the reference waveform. You can directly click or tap the icons at the right side of the input field of VScale to increase or decrease the vertical scale value. You can also use the corresponding multipurpose knob to adjust the scale.

**Modify the Vertical Offset**

Click or tap the input field of VOffset, and then use the pop-up numeric keypad to set the vertical offset of the reference waveform. You can directly click or tap the Up and Down arrow icons at the right side of the input field of VOffset to
increase or decrease the vertical offset value. You can also use the corresponding multipurpose knob to adjust the offset.

**Restore the Reference Waveform**

If you have adjusted the vertical scale and offset for the specified reference waveform of the current channel, to reset the reference waveform to the position where the source channel stays prior to the SaveToRef operation, click or tap Reset.

**Set the Reference Waveform Color**

This series oscilloscope provides five colors (gray, green, light blue, red, and orange) to mark the reference waveforms of different channels in order to distinguish them.

Click or tap the drop-down button of Color to select the color of the reference waveform of the channel.

**Set the Reference Waveform Label**

Click or tap the Label on/off switch to enable or disable the label display of the specified reference waveform.

Click or tap the input field of Label to set the label of the specified reference channel with the pop-up numeric keypad.

## 13.4 Export and Import Operation

**Export to Internal or External Memory**

You can save the current reference waveform to the internal memory or external USB storage device. The file format of the reference waveform is "*.ref", "*.bin", or "*.csv".

Click or tap Export to enter the reference waveform file saving interface.

• **Set the Format**

In the file saving interface, click or tap the drop-down button of Format to select "*.ref", "*.bin", or "*.csv" as the saving format.

• **Set the Filename**

Click or tap the input field of File Name to set the filename with the pop-up virtual keypad.

For how to use the keypad, refer to descriptions in Parameter Setting Method.

• **Set the Save Path**

Click or tap the File Path input field, then the disk management menu is displayed. Through the disk management menu, you can save the current
reference waveform to the internal memory or external USB storage device. Then click or tap Save to complete the save operation. For details about the disk management operation, refer to the Disk Management section in Store and Load.

**TIP**

• Only when the reference waveform is saved, can this export function be valid.

• For the ".bin" format file, refer to Binary Data Format (.bin).

**Import from Internal or External Memory**

You can import the stored reference waveform file from the internal memory or external USB storage device to the instrument and display the file on the screen.

Click or tap Import to enter the reference waveform file loading interface.

• **Set the Format**

The file format of the reference waveform is specified as "*.ref" which is displayed in Format.

• **Set the Load Path**

Click or tap the input field of File Path, then the disk management interface is displayed.

Through the disk management menu, you can load the current reference waveform to the waveform view of the oscilloscope. Then click or tap Load to complete the load operation. For details about the disk management operation, refer to the Disk Management section in Store and Load.

# 14 Pass/Fail Test

During the product design and manufacturing process, you usually need to monitor the variations of the signal or judge whether the product is up to standard. This series oscilloscope can accomplish this task perfectly with its standard pass/fail test function. You can use this function to define the mask based on "standard" waveforms. It compares the signal under test with the mask and displays the test results. When the pass/fail status is detected, you can choose to stop monitoring, sound an alarm with the beeper, or save the current screen image.

Click or tap the function navigation icon at the lower-left corner of the screen to open the function navigation. Then click or tap the Pass/Fail button to enter the "PassFail" setting menu. You can also press the front-panel key and select Pass/Fail to enter the "PassFail" setting menu. The menu is as shown in the figure below.

Figure 14.1 PassFail Menu

Click or tap to minimize the "PassFail" menu to simplify the display, as shown in the figure below.

Figure 14.2 PassFail Menu-Simplified
## 14.1 To Enable or Disable the Pass/Fail Test Function

In the "Pass/Fail" setting menu, click or tap the Enable on/off switch to enable or disable the pass/fail test function.

You can select the source, create mask, and set test result output only after the pass/fail test function is enabled.

## 14.2 To Select the Source

Click or tap the drop-down button of Source to select the desired source. The available output channels include CH1-CH4.

**TIP**

When a disabled channel is selected as the source, it will be automatically turned on.

## 14.3 To Create a Mask

In the Pass/Fail menu, you can self-define the mask of the pass/fail test. The mask can be imported or exported.

**Create a Mask**

Click or tap X Mask and Y Mask input fields respectively to set the horizontal tolerance range and vertical tolerance range with the pop-up numeric keypad. You can also use the icons at the right side of the input fields or use the corresponding multipurpose knob to set the values. Then click or tap Create to apply the currently created mask (the region not covered by blue within the screen).

**Save the Mask**

When the pass/fail test function is enabled, you can save the current test mask range to the internal memory or an external USB storage device (when detected) in "*.pf" format.

Click or tap Save to enter the file saving interface. Click or tap the input field of File Name and File Path to input the filename and select the desired file path to save the test mask file to the internal or external memory. For details, refer to the Disk Management section in Store and Load.

**Load a Mask**

When the pass/fail test function is enabled, you can load the test mask files from the internal memory or an external USB storage device (when detected) and apply them to the current pass/fail test function.
Click or tap Load to enter the file loading interface. Click or tap the input field of File Path to load the specified test mask files (in *.pf format) and apply them to the current pass/fail test function. For details, refer to the Disk Management section in Store and Load.

## 14.4 To Set the Output Form of the Test Results

In Option, you can set what the oscilloscope will execute when test results are detected according to your needs.

**Set the output event and Aux output**

• Click or tap the Aux Output on/off switch to enable or disable the Aux output. When enabled, in the Utility menu, the sub-menu AUX Out of Setup is automatically set to "PassFail". When a successful or failed event is detected, a pulse will be output from the rear-panel [AUX OUT] connector. When disabled, the sub-menu AUX Out of Setup in the Utility menu is automatically set to "TrigOut", and the output of the [AUX OUT] connector is irrelevant with the pass/fail test.

• Select "Pass" or "Fail" in Output Event. When a "pass" or "fail" event is detected, a pulse will be output from the rear-panel [AUX OUT] connector.

**Set the output polarity and output pulse width**

Select "Positive" or "Negative" in Polarity, then click or tap the input field of Pulse to set the pulse width with the pop-up numeric keypad. You can also use the corresponding multipurpose knob to set the value. Its range is from 100 ns to 10 ms. By default, it is 1 μs.

**Set the error action**

In Err Action, select one operation that the oscilloscope will execute once a pass/fail test is detected.

• Stop: stop sampling when a failed event is found.

• Beeper: the beeper sounds an alarm when a failed event is found (irrelevant with the on/off status of the beeper).

• Screenshot: perform the screenshot operation when a failed event is found. If an external storage device is detected, the screenshot will be saved to the external storage device directly. Otherwise, it will be saved to the local disk.

If "Screenshot" is selected, "Stop" action will be executed forcibly. The sampling stops automatically. After the screenshot operation is completed, the sampling will continue.
## 14.5 To Start or Stop the Pass/Fail Test Operation

After the Pass/Fail test function is enabled, click or tap the Operate button to start the test operation or to stop the operation.

During the test process, the oscilloscope will test the waveforms, display the test information, and output the test information based on the current settings. The "Pass/Fail" result will be displayed in the "Result" bar at the right side of the screen, as shown in the figure below.

Figure 14.3 Pass/Fail Test Interface

**TIP**

• Only when the pass/fail test function is enabled, can you start or stop the pass/fail test operation, save and load the mask range.

• After starting the test operation, you can neither modify the source channel nor adjust the test mask.

## 14.6 To Display the Statistics of the Test Results

After the "Pass/Fail" function is enabled, the test results will be displayed in the "Result" bar at the right side of the screen. You can click or tap the icon at the lower-right corner of the screen to hide the "Result" sidebar.

The test results statistics include the number of failed frames, the number of successful frames, and total number of frames, as shown in the figure below.

The test results display shows:
- Failed Frames
- Passed Frames  
- Total Frames
Click or tap the "Pass/Fail" label and a window is displayed for you to perform the following operations.

• Click or tap Reset Stat., and then the statistics in the "Pass/Fail" label will be reset to 0.

• Click or tap Setting, and then the PassFail setting menu is displayed.

• Click or tap Remove, and then the pass/fail function is disabled.

# 15 Protocol Decoding

You can use the protocol analysis to discover errors, debug hardware, and accelerate development easily, ensuring you to accomplish the projects with high speed and good quality. Protocol decoding is the basis of protocol analysis. Only protocol analyses with correct protocol decoding are acceptable, and only correct protocol decoding can identify more error information. This oscilloscope provides four bus decoding modules (Decode 1, Decode 2, Decode 3, and Decode 4) to make common protocol decoding for the input signals of the analog channels. It provides standard serial decodes including Parallel, RS232/UART, I2C, SPI, and CAN. As the decoding functions and setting methods of Decode1, Decode2, Decode3, and Decode4 are the same, this chapter takes Decode1 as an example for illustration.

• Click or tap > Decode to enter the "Decode" menu.

• Click or tap the Decode button on the toolbar to enter the "Decode" menu.

## 15.1 Parallel Decoding

Parallel bus consists of clock line and data line. As shown in the figure below, CLK is the clock line, whereas Bit0 and Bit1 are the 0 bit and 1st bit on the data line respectively. The oscilloscope will sample the channel data on the rising edge, falling edge, or the rising/falling edge of the clock and judge each data point (logic "1" or logic "0") according to the preset threshold level.

```
CLK     ┌─┐   ┌─┐   ┌─┐   ┌─┐   ┌─┐
        │ │   │ │   │ │   │ │   │ │
        ┘ └───┘ └───┘ └───┘ └───┘ └

Bit0    ┌─────┐     ┌─────┐     
        │     │     │     │     
        ┘     └─────┘     └─────

Bit1    ┌─────┐     ┌─────┐     ┌─────
        │     │     │     │     │     
        ┘     └─────┘     └─────┘     

Parallel[BIN]  11    10    10    10    00
```

Figure 15.1 Schematic Diagram of Parallel Decoding

In the Decode menu, click or tap the drop-down button of Bus Type to select Parallel, then configure the parameters for Parallel decoding.
Figure 15.2 Parallel Decoding Menu

**Bus Status**

Click or tap the Bus Status on/off switch to enable or disable the bus decoding.

### 15.1.1 Clock Setting (CLK)

**Clock Setting (CLK)**

Click or tap the drop-down button of CLK to select from analog channels CH1-CH4. If "OFF" is selected, no clock channel is set, and sampling is performed when a hop occurs to the data of the data channel during decoding.

**Threshold**

You need to set a threshold when the clock signal is an analog channel (CH1-CH4). Click or tap the input field of Threshold, and then use the pop-up numeric keypad to set the threshold. You can also use the corresponding multipurpose knob to set the value. The range of the threshold is related to the current vertical scale and offset.

**CLK Edge**

You can select "Rising", "Falling", or "Both" in CLK Edge when the clock channel is set to an analog channel (CH1-CH4).

• Rising: samples the channel data on the rising edge of the clock.

• Falling: samples the channel data on the falling edge of the clock.

• Both: samples the channel data on the rising edge or the falling edge of the clock.
### 15.1.2 Bus Setting

**Set the Bus**

Click or tap the drop-down button of BUS to select the desired bus. Available options include analog channels CH1-CH4. You can also self-define the bus.

Table 15.1 Bus Setting

| Bus | Width | Bit X | Channel | Remarks |
|-----|-------|-------|---------|---------|
| CH1 | 1 | 0 | CH1 | Width, Bit X, and CH are set automatically, and you cannot modify them. |
| CH2 | 1 | 0 | CH2 | Width, Bit X, and CH are set automatically, and you cannot modify them. |
| CH3 | 1 | 0 | CH3 | Width, Bit X, and CH are set automatically, and you cannot modify them. |
| CH4 | 1 | 0 | CH4 | Width, Bit X, and CH are set automatically, and you cannot modify them. |
| User | 1 (Default) to 4 | 0 (Default) | - | - |

**Set the Width**

When the "BUS" setting is set to "User", you can set the bus width. Click or tap the input field of Width, and then use the pop-up numeric keypad to set the width. You can also use the corresponding multipurpose knob to set the value.

**Specify data channel for each bit**

When the "BUS" setting is set to "User", you can specify the data channel for each bit.

Click or tap Bit X set the bit of the channel. By default, 0 is selected. Its available range is from 0 to (width - 1).

Click or tap the drop-down button of CH to select the data channels for a bit. Available sources include analog channels CH1-CH4.
**Set the Threshold Level**

To judge logic "1" and logic "0" of the buses, you need to set a threshold for each analog channel (CH1-CH4). When the channel signal amplitude is greater than the preset threshold, it is judged as logic "1"; otherwise logic "0".

Click or tap the input field of Threshold, and then use the pop-up numeric keypad to set the threshold. You can also use the corresponding multipurpose knob to set the value. The range of the threshold is related to the current vertical scale and offset.

**Set the endian**

In Endian, select "Invert" or "Normal" as the endian of the bus.

**Set the polarity**

In Polarity, select "Positive" or "Negative" as the data polarity.

### 15.1.3 Display-related Settings

In Decode menu, set the following display-related parameters.

**Set the Display Format**

Click or tap the drop-down button of Format to select the display format of the bus data and event table. The available options include "Hex", "Dec", "Bin", and "ASCII".

**Set the Label Display**

Click or tap the Label on/off switch to enable or disable the label display of the decoding bus. When enabled, the bus label will be displayed at the upper-left side of the bus (when the bus display is enabled). The label shows the current bus type.

### 15.1.4 Event Table

The event table displays the decoded data and the corresponding decoding information in time order in the form of a table. It can be used to observe relatively longer decoded data. The decoding information includes the decoded data, the corresponding line number, and time information.
**Open or Close the Event Table**

Click or tap the Event Table on/off switch to enable or disable the display of the event table. When enabled, the event table is displayed as shown in the figure below.

You can also click or tap the icon at the upper-right corner of the table to close the event table.

Figure 15.3 Parallel Decoding Event Table

**TIP**

• When you adjust the horizontal time base, the waveform displayed on the screen will also change, and the total number of lines containing the decoding information in the event table will also be changed.

• The displayed decoded data information in the bus is related to the value of the horizontal time base. Reducing the horizontal time base can help you view the detailed information.

**Export**

When the oscilloscope is in "STOP" state, you can export the time and its corresponding decoded data in the event table.

In Decode menu, click or tap Export, then the save setting interface is displayed. You can export the data to the internal memory or the external USB storage device (only when detected) in *.csv format. For details, refer to Store and Load.

## 15.2 RS232 Decoding

RS232 serial bus consists of the transmitting data line (TX) and the receiving data line (RX).
Figure 15.4 Schematic Diagram of RS232 Serial Bus

In RS232, baud rate is used to represent the transmission rate (namely bits per second) of the data. You need to set the start bit, data bits, check bit (optional), and stop bits for each frame of data.

• Start Bit: indicates when to output data.

• Data Bit: indicates the number of data bits actually contained in each frame of data.

• Check Bit: used to check whether the data are properly transmitted.

• Stop Bit: indicates when to stop outputting data.

In the Decode menu, click or tap the drop-down button of Bus Type to select RS232, then configure the parameters for RS232 decoding.

Figure 15.5 RS232 Decoding Menu
**Bus Status**

Click or tap the Bus Status on/off switch to enable or disable the bus decoding.

**Quickly Apply Trigger Settings to Decoding**

Copy trig indicates applying the trigger settings to the specified decoding setting.

Click or tap Copy Trig to apply the trigger settings to the specified decoding setting.

### 15.2.1 Source Setting

**Set the Tx source and the threshold**

Click or tap drop-down button of Tx to select the desired source. The options include CH1-CH4 and OFF.

When the source is set to CH1-CH4, you can click or tap the input field of Threshold, and then use the pop-up numeric keypad to set the threshold of Tx source. You can also use the corresponding multipurpose knob to set the value. The range of the threshold is related to the current vertical scale and offset.

When you modify the threshold of the Tx source channel, a dotted line displaying the current threshold level is displayed on the screen. It disappears in about 2 s after you stop modifying the threshold.

**Set the Rx source and the threshold**

Use the same method to select the Rx source and set the threshold. The default state of Rx is OFF.

**TIP**

The sources of Tx and Rx cannot be set to OFF at the same time.

**Polarity**

Click or tap "Positive" or "Negative" in Polarity.

• Positive: High level is logic "1" and low level is logic "0".

• Negative: High level is logic "0" and low level is logic "1".

**Set the baud rate**

Click or tap the drop-down button of Baud to select the baud rate. The available baud rates include 50 bps, 75 bps, 110 bps, 134 bps, 150 bps, and etc.

The oscilloscope allows you to self-define the baud rate. Click or tap the drop-down button of Baud to select "User" and then set the baud rate with the pop-up numeric keypad.
### 15.2.2 To Set Data Package

**Data**

Click or tap the drop-down button of Data to select the data bits. The available data bits are 5 bits, 6 bits, 7 bits, 8 bits, and 9 bits.

**Parity**

It is used to check whether the data transmission is correct. Click or tap the dropdown button of Parity to select the desired parity mode.

• None: indicates that no check bit appears during the transmission.

• Even: indicates that the total number of "1" in the data bit and check bit is an even number. For example, when 0x55 (01010101) is sent, "0" should be added to the check bit.

• Odd: indicates that the total number of "1" in the data bit and check bit is an odd number. For example, when 0x55 (01010101) is sent, "1" should be added to the check bit.

**Stop Bit**

Click or tap the drop-down button of Stop Bit to set the stop bits after each frame of data. It can be set to 1 bit, 1.5 bits, or 2 bits.

**Endian**

Click or tap the drop-down button of Endian to select the desired endian.

• LSB: indicates Least Significant Bit transmission sequence, i.e. the lowest bit of the data is transmitted first.

• MSB: indicates Most Significant Bit transmission sequence, i.e. the highest bit of the data is transmitted first.

```
bit0 bit1 bit2 bit3 bit4 bit5 bit6 bit7     bit7 bit6 bit5 bit4 bit3 bit2 bit1 bit0
←─────────────── t ──────────────→         ←─────────────── t ──────────────→
              LSB                                        MSB
```

### 15.2.3 Display-related Settings

In Decode menu, set the following display-related parameters.
**Set the Display Format**

Click or tap the drop-down button of Format to select the display format of the bus data and event table. The available options include "Hex", "Dec", "Bin", and "ASCII".

**Set the Label Display**

Click or tap the Label on/off switch to enable or disable the label display of the decoding bus. When enabled, the bus label will be displayed at the upper-left side of the bus (when the bus display is enabled). The label shows the current bus type.

### 15.2.4 Event Table

Click or tap the Event Table on/off switch to enable or disable the display of the event table. When enabled, the event table is displayed as shown in the figure below.

You can also click or tap the icon at the upper-right corner of the table to close the event table.

Figure 15.6 RS232 Decoding Event Table

**TIP**

• When you adjust the horizontal time base, the waveform displayed on the screen will also change, and the total number of lines containing the decoding information in the event table will also be changed.

• The displayed decoded data information in the bus is related to the value of the horizontal time base. Reducing the horizontal time base can help you view the detailed information.

**Export**

When the oscilloscope is in "STOP" state, you can export the time and its corresponding decoded data in the event table.
In Decode menu, click or tap Export, then the save setting interface is displayed. You can export the data to the internal memory or the external USB storage device (only when detected) in *.csv format. For details, refer to Store and Load.

## 15.3 I2C Decoding

I2C serial bus consists of the clock line (SCL) and the data line (SDA).

SCL: samples SDA on the rising or falling edge of the clock.

SDA: indicates the data channel.

Figure 15.7 I2C Serial Bus

In the Decode menu, click or tap the drop-down button of Bus Type to select I2C, then configure the parameters for I2C decoding.

Figure 15.8 I2C Decoding Menu

**Bus Status**

Click or tap the Bus Status on/off switch to enable or disable the bus decoding.

**Quickly Apply Trigger Settings to Decoding**

Copy trig indicates applying the trigger settings to the specified decoding setting.

Click or tap Copy Trig to apply the trigger settings to the specified decoding setting.
### 15.3.1 Source Setting

**Set the clock channel source and the threshold**

• Click or tap the drop-down button of CLK to select the desired source of the clock channel. Available sources include analog channels CH1-CH4.

• Click or tap the input field of SCL Thre and use the pop-up numeric keypad to set the threshold of the clock channel. You can also use the corresponding multipurpose knob to set the value.

When you modify the threshold of the clock channel, a dotted line displaying the current threshold level is displayed on the screen. It disappears in about 2 s after you stop modifying the threshold.

**Set the data channel source and the threshold**

• Click or tap the drop-down button of SDA to select the desired source of the data channel. Available sources include analog channels CH1-CH4.

• Click or tap the input field of SDA Thre and use the pop-up numeric keypad to set the threshold of the data channel. You can also use the corresponding multipurpose knob to set the value.

**Exchange sources**

Select "SCL/SDA" or "SDA/SCL" in Exchange to exchange the sources of the current clock channel and data channel.

**Specify whether the address information includes the "R/W" bit**

For I2C bus, each frame of data starts with the address information (read address and write address).

Select "Without" or "With" in R/W to decide whether the address information includes the "R/W" bit. When "With" is selected, the "R/W" bit will be included in the address information; when "Without" is selected, the "R/W" bit will not be included in the address information.

### 15.3.2 Display-related Settings

In Decode menu, set the following display-related parameters.

**Set the Display Format**

Click or tap the drop-down button of Format to select the display format of the bus data and event table. The available options include "Hex", "Dec", "Bin", and "ASCII".
**Set the Label Display**

Click or tap the Label on/off switch to enable or disable the label display of the decoding bus. When enabled, the bus label will be displayed at the upper-left side of the bus (when the bus display is enabled). The label shows the current bus type.

### 15.3.3 Event Table

**Open or Close the Event Table**

Click or tap the Event Table on/off switch to enable or disable the display of the event table. When enabled, the event table is displayed as shown in the figure below.

You can also click or tap the icon at the upper-right corner of the table to close the event table.

Figure 15.9 I2C Decoding Event Table

**TIP**

• When you adjust the horizontal time base, the waveform displayed on the screen will also change, and the total number of lines containing the decoding information in the event table will also be changed.

• The displayed decoded data information in the bus is related to the value of the horizontal time base. Reducing the horizontal time base can help you view the detailed information.

**Export**

When the oscilloscope is in "STOP" state, you can export the time and its corresponding decoded data in the event table.

In Decode menu, click or tap Export, then the save setting interface is displayed. You can export the data to the internal memory or the external USB storage device (only when detected) in *.csv format. For details, refer to Store and Load.
**Address information in decoding**

For I2C bus, each frame of data starts with the address information (read address and write address). In the address information, "Read" indicates the read address ( ) and "Write" indicates the write address ( ). You can decide whether to include or exclude the "R/W" bit for the address information.

**Error expressions in decoding**

In I2C decoding, the response includes ACK (acknowledgment) and NACK (non-acknowledgment). When NACK is detected after "Write", red error report information ( ) is displayed.

## 15.4 SPI Decoding

SPI bus is based on the master — slave configuration and usually consists of chip select line (CS), clock line (CLK), and data line (SDA). Wherein, the data lines include the master input/slave output (MISO) data line and master output/slave input (MOSI) data line. The oscilloscope samples the channel data on the rising or falling edge of the clock signal and judge each data point (logic "1" or logic "0") according to the preset threshold level.

Figure 15.10 SPI Serial Bus

In the Decode menu, click or tap the drop-down button of Bus Type to select SPI, then configure the parameters for SPI decoding.
Figure 15.11 SPI Decoding Menu

**Bus Status**

Click or tap the Bus Status on/off switch to enable or disable the bus decoding.

**Quickly Apply Trigger Settings to Decoding**

Copy trig indicates applying the trigger settings to the specified decoding setting.

Click or tap Copy Trig to apply the trigger settings to the specified decoding setting.

### 15.4.1 To Set the Source

**Set the Clock Signal**

• Click or tap the drop-down button of CLK to select the desired source of the clock channel. Available sources include analog channels CH1-CH4.

• Click or tap the input field of Threshold at the right side of CLK and use the pop-up numeric keypad to set the threshold of the clock channel. You can also use the corresponding multipurpose knob to set the value.

• Click or tap "Rising" or "Falling" in Slope to set the instrument to sample MISO and MOSI on the CLK edge.

**MISO and MOSI Setting**

• Click or tap the drop-down button of MISO to select the desired source. Available sources include analog channels CH1-CH4 and OFF.

• When the MISO source is set to CH1-CH4, you can click or tap the input field of Threshold at the right side of MISO, and then use the pop-up numeric keypad to set the threshold of the MISO channel. You can also use the corresponding multipurpose knob to set the value.
• Click or tap the drop-down button of MOSI to select the desired source. Available sources include analog channels CH1-CH4 and OFF.

• When the MOSI source is set to CH1-CH4, you can click or tap the input field of Threshold at the right side of MOSI, and then use the pop-up numeric keypad to set the threshold of the MOSI channel. You can also use the corresponding multipurpose knob to set the value.

**TIP**

The MISO and MOSI sources cannot be set to "OFF" at the same time.

### 15.4.2 To Set Mode and Data

**Mode**

Select "Timeout" or "CS" in Mode.

• **Timeout**

You can perform frame synchronization according to the timeout, and the timeout value must be greater than half of the clock cycle Click or tap the input field of Timeout, and then use the pop-up numeric keypad to set the timeout value. You can also use the corresponding multipurpose knob to set the value. The adjustable range of the timeout value is from 8 ns to 10 s. By default, it is 1 μs.

• **CS**

It contains a chip select line (CS). You can perform frame synchronization according to CS. When "CS" is selected,

- Click or tap the drop-down button of CS to select the desired source. The sources include analog channels CH1-CH4.

- Click or tap the input field of Threshold and use the pop-up numeric keypad to set the threshold. You can also use the corresponding multipurpose knob to set the value.

- In CS Polarity, select "Positive" or "Negative".

**NOTE**

As DHO812/DHO802 only has two channels, the CS mode is not available.

**Endian**

Click or tap the drop-down button of Endian to select the desired endian.
• LSB: indicates Least Significant Bit transmission sequence, i.e. the lowest bit of the data is transmitted first.

• MSB: indicates Most Significant Bit transmission sequence, i.e. the highest bit of the data is transmitted first.

```
bit0 bit1 bit2 bit3 bit4 bit5 bit6 bit7     bit7 bit6 bit5 bit4 bit3 bit2 bit1 bit0
←─────────────── t ──────────────→         ←─────────────── t ──────────────→
              LSB                                        MSB
```

**Polarity**

In Polarity, select "Positive" or "Negative" as the data polarity.

**Width Setting**

Click or tap the input field of Width, and then use the pop-up numeric keypad to set the length of the data. You can also use the corresponding multipurpose knob to set the value. The setting range is from 4 to 32. By default, it is 8.

### 15.4.3 Display-related Settings

In Decode menu, set the following display-related parameters.

**Set the Display Format**

Click or tap the drop-down button of Format to select the display format of the bus data and event table. The available options include "Hex", "Dec", "Bin", and "ASCII".

**Set the Label Display**

Click or tap the Label on/off switch to enable or disable the label display of the decoding bus. When enabled, the bus label will be displayed at the upper-left side of the bus (when the bus display is enabled). The label shows the current bus type.

### 15.4.4 Event Table

**Open or Close the Event Table**

Click or tap the Event Table on/off switch to enable or disable the display of the event table. When enabled, the event table is displayed as shown in the figure below.

You can also click or tap the icon at the upper-right corner of the table to close the event table.
Figure 15.12 SPI Decoding Event Table

**TIP**

• When you adjust the horizontal time base, the waveform displayed on the screen will also change, and the total number of lines containing the decoding information in the event table will also be changed.

• The displayed decoded data information in the bus is related to the value of the horizontal time base. Reducing the horizontal time base can help you view the detailed information.

**Export**

When the oscilloscope is in "STOP" state, you can export the time and its corresponding decoded data in the event table.

In Decode menu, click or tap Export, then the save setting interface is displayed. You can export the data to the internal memory or the external USB storage device (only when detected) in *.csv format. For details, refer to Store and Load.

## 15.5 CAN Decoding

The oscilloscope samples the CAN signal at the specified sample position, and judges each data point to be logic "1" or logic "0" according to the preset threshold level. You need to specify the CAN signal type and sample position.

In the Decode menu, click or tap the drop-down button of Bus Type to select CAN, then configure the parameters for CAN decoding.
Figure 15.13 CAN Decoding Menu

**Bus Status**

Click or tap the Bus Status on/off switch to enable or disable the bus decoding.

**Quickly Apply Trigger Settings to Decoding**

Copy trig indicates applying the trigger settings to the specified decoding setting.

Click or tap Copy Trig to apply the trigger settings to the specified decoding setting.

### 15.5.1 Signal Configuration

**Set the source and the threshold**

• Click or tap the drop-down button of Source to select analog channels CH1-CH4.

• Click or tap the input field of Threshold, and then use the pop-up numeric keypad to set the threshold of the source channel or use the corresponding multipurpose knob to set the value.

When you modify the threshold of the signal source, a dotted line displaying the current threshold level is displayed on the screen. It disappears in about 2 s after you stop modifying the threshold.

**Select the Signal Type**

Click or tap the drop-down button of Signal to select a signal type that matches the CAN bus signal. The available signal types include CAN_H, CAN_L, Rx, Tx, and Diff.

• CAN_H: indicates the actual CAN_H bus signal.

• CAN_L: indicates the actual CAN_L bus signal.

• Rx: indicates the Receive signal from the CAN bus transceiver.

• Tx: indicates the Transmit signal from the CAN bus transceiver.
• **DIFF**: The CAN differential bus signals connected to an analog source channel by using a differential probe. Connect the probe's positive lead to the CAN_H bus signal and connect the negative lead to the CAN_L bus signal.

**Specify the Standard Signal Rate**

Click or tap the drop-down button of Baud to select the preset baud rate. The available baud rates include 10.0 kbps, 19.2 kbps, 20.0 kbps, 33.3 kbps and etc. This instrument also supports user-defined baud rate. Click or tap the Baud drop-down button to select "User" and set the baud rate with the pop-up numeric keypad.

**Sample Position**

Sample position is a point within a bit's time. The oscilloscope samples the bit level at this point. The sample position is represented by the proportion of "the time from the start of the bit to the sample point" to the "bit time", as shown in the figure below.

Figure 15.14 Sample Position

Click or tap the Sample Position input field and use the pop-up numeric keypad to set the value. You can also use the corresponding multipurpose knob to set the value. The settable range is from 10% to 90%.

### 15.5.2 Display-related Settings

In Decode menu, set the following display-related parameters.

**Set the Display Format**

Click or tap the drop-down button of Format to select the display format of the bus data and event table. The available options include "Hex", "Dec", "Bin", and "ASCII".

**Set the Label Display**

Click or tap the Label on/off switch to enable or disable the label display of the decoding bus. When enabled, the bus label will be displayed at the upper-left side of the bus (when the bus display is enabled). The label shows the current bus type.
### 15.5.3 Event Table

**Open or Close the Event Table**

Click or tap the Event Table on/off switch to enable or disable the display of the event table. When enabled, the event table is displayed as shown in the figure below.

You can also click or tap the icon at the upper-right corner of the table to close the event table.

Figure 15.15 CAN Decoding Event Table

**TIP**

• When you adjust the horizontal time base, the waveform displayed on the screen will also change, and the total number of lines containing the decoding information in the event table will also be changed.

• The displayed decoded data information in the bus is related to the value of the horizontal time base. Reducing the horizontal time base can help you view the detailed information.

**Export**

When the oscilloscope is in "STOP" state, you can export the time and its corresponding decoded data in the event table.

In Decode menu, click or tap Export, then the save setting interface is displayed. You can export the data to the internal memory or the external USB storage device (only when detected) in *.csv format. For details, refer to Store and Load.

**Interpret the Decoded CAN Data**

• Frame ID: expressed in Hex, identified as "ID:".

• DLC (Data Length Code): expressed in Hex, identified as "DLC:".

• Data: Its display format is the same as that of the bus data (Hex, Dec, Bin, or ASCII), identified as "Data:".
• CRC (Cyclic Redundancy Check): expressed in Hex, identified as "CRC:".

• ACK (Acknowledgement): identified as "ACK". When errors (ACK is detected to be 1) occur, displayed as a red patch.

• R (remote frame): identified as "R:".

• Stuff (Bit filling error): identified as "Stuff".

# 16 Multi-pane Windowing

This series oscilloscope supports multi-pane windowing. You can add multiple windows and result display windows for display and view.

Click or tap > Windows to enter the "Add Window" menu. You can also click or tap the Windows button on the toolbar at the top of the screen to enter the menu, as shown in the figure below.

Figure 16.1 "Add Window" Menu

## Add Diagram Windows

1. First, select "XY" or "Math" in Diagram. When a diagram is selected, its preview and parameter setting items can be displayed at the upper part of the "Add Window" menu.

2. You can set the corresponding parameters according to your needs. For details, refer to descriptions of relevant chapters.

3. Click or tap Add and then the selected diagram is displayed on the screen.
**TIP**

When the waveform view window is closed, the "Waveform View" item appears on the Diagram menu. You can use the item to open the waveform view window.

## Add Result Table Window

Click or tap "Measure", "All Measure", or "Decode" in Result Table, and then click or tap Add. The corresponding measurement results will be displayed on the screen.

# 17 Waveform Recording and Playing

Waveform recording/playing function can play the recorded waveforms, enabling you to analyze the waveforms better.

You can enter the "Record" menu in the following ways.

• Click or tap the function navigation icon and then select Record to enter the "Record" menu.

• Click or tap Record on the toolbar to enter the "Record" menu.

• Press the front-panel key and select Record in the pop-up "Analyse" menu to enter the "Record" menu.

Figure 17.1 "Record" Menu

**TIP**

When the acquisition mode is set to UltraAcquire, the waveform recording/playing function is not available. You can view waveform segments using Navigate segments.

## 17.1 Common Settings

**Waveform Recording**

Click or tap the Record on/off switch to enable or disable the waveform recording function. Before recording the waveform, you can refer to descriptions in Record Options to set the waveform recording parameters.
• Click or tap the Record button to start recording the waveforms. Then the record icon turns into from .

• The data at the right side of the record progress bar indicate the current frame/ total frames. During recording, the current recording information is displayed on the screen in real time with the current frames constantly changing.

• After the recording is completed, turns into and recording stops automatically.

• During recording, you can also click or tap to suspend the recording manually.

Currently Recorded Frames Total Frames

**Waveform Playing**

Click or tap the play icon in Play to start playing the recorded waveforms. Then the play icon turns into from . For details about playing, refer to descriptions in Play Options. During waveform playing, the value in Current changes dynamically.

During playing, you can also click or tap the icon again to suspend playing manually. ∆T indicates the time interval between the current frame and the first frame during the recording process.

## 17.2 Record Options

During the waveform recording, the oscilloscope records the waveforms of the currently enabled channel at a specified interval until you manually stops the recording operation or the number of recorded frames has reached the limit.

Before recording the waveforms, set the following parameters.

**1. Interval**

The recording interval indicates the time interval between the frames during the recording process.

Click or tap the Interval input field and use the pop-up numeric keypad to set the time interval between frames. You can also use the front-panel multipurpose knob to set the value. The available range is from 10 ns to 1 s.

**2. Frames**

The recording frames refer to the number of frames that can be recorded actually. After starting the recording operation, the oscilloscope stops the recording
operation automatically when the number of recorded frames reaches the set value.

Click or tap the Frames input field to set the number of waveform frames to be recorded currently. You can also use the front-panel multipurpose knob to set the value. The range available is from 1 to the maximum number of frames that can be recorded currently.

**3. Max Frames**

The input field of Max Frames displays the maximum number of frames that can be recorded currently. Click or tap Max and the frames will be automatically set to the maximum value.

As the waveform memory is fixed, the more points in each frame, the fewer waveform frames that can be recorded. Therefore, the maximum number of recorded frames depends on currently selected "memory depth" (refer to Memory Depth). The number of waveform points per frame is the current memory depth.

Memory Depth ≥ Sample Rate x Horizontal Time Base x Number of Grids in the Horizontal Direction. Therefore, the Max. value of waveform recording is also related to the "Sample Rate" and "Horizontal Time Base".

**4. Beeper**

: the beeper sounds at the end of recording.

: the beeper does not sound at the end of recording.

## 17.3 Play Options

Waveform playing function can play back the waveforms currently recorded. In Play, click or tap the Minimize on/off switch to select whether to minimize the menu. When ON is selected, the window is minimized, making the display more simplified, easy for observation and operation. The minimized menu is as shown in the figure below.
Figure 17.2 Minimized "Play" Menu

Before playing the waveforms, set the following parameters.

**1. Play Mode**

You can play the waveforms in single mode (🔄) or cycle mode (🔁).

- 🔄: plays from the start frame to the end frame, and then stops automatically.

- 🔁: plays from the start frame to the end frame, then such playback operation is repeated until you stop it manually.

**2. Play Sequence**

You can play back the waveforms clockwise (▶️) or counterclockwise (◀️).

- ▶️: plays from the start frame to the end frame.

- ◀️: plays from the end frame to the start frame.

**3. Interval**

The playback interval indicates the time interval between the frames during the playing process.

Click or tap the input field of Interval, and then use the pop-up numeric keypad to set the time interval between frames. You can also use the corresponding multipurpose knob to set the value. The available range is from 1 ms to 1 s.

**4. Start Frame**
Click or tap the "Start Frame" input field in Figure 17.2 to set the start frame for playing back the waveforms. You can also use the corresponding multipurpose knob to set the value. The default is 1, and the maximum value is the maximum number of frames recorded.

**5. End Frame**

Click or tap the "End Frame" input field in Figure 17.2 to set the end frame for playing back the waveforms. You can also use the corresponding multipurpose knob to set the value. The default is the number of frames of the recorded waveforms.

**6. Current Frame**

When the playing is stopped, click or tap the "Current" input field in Figure 17.2 to set the currently displayed frame with the pop-up numeric keypad. You can also use the corresponding numeric keypad to set the value. The maximum allowed is the number of recorded frames.
# 18 Search and Navigation

The Search function allows you to quickly find and mark the event of interest and then go to the specified event in the marktable by navigating search events. The search types include edge and pulse.

The Navigation function allows you to navigate time, search events, and segments.

## 18.1 Search

This function allows you to search for the specified edge and pulse width trigger events. Found search events are marked with small inverted triangles (▼) at the top of the graticule. Click or tap > Search to enter the "Search" menu. You can also click or tap Search in the "Navigation" menu (only when the navigation mode is set to "Search Event") to enter the "Search" menu, as shown in the figure below.

Figure 18.1 Search Menu

**1. Search On/Off**

Click or tap Search on/off switch to enable or disable the search function.

**TIP**

Enabling the search function automatically turns on the Zoom Mode (Delayed Sweep).

**2. Set up searches**
Click or tap the Type drop-down button to select "Edge" or "Pulse". Click or tap the Source drop-down button to select the source.

- Edge Searches: After setting the search type to "Edge", you can select the slope type. For details, please refer to Edge Trigger. You can click or tap the Threshold input filed to set the threshold with the pop-up numeric keypad or use the corresponding multipurpose knob to set the value.

- Pulse Width Searches: After setting the search type to "Pulse", you can set the trigger condition. For details, please refer to Pulse Width Trigger. You can click or tap the Threshold input filed to set the threshold with the pop-up numeric keypad or use the corresponding multipurpose knob to set the value.

**3. Copy search setups**

- Copy to Trigger
Click or tap To Trigger to copy the setup for the selected search type to the same trigger type. For example, if the current search type is "Edge", clicking or tapping To Trigger copies the search settings to the "Edge Trigger" settings.

- Copy from Trigger
Click or tap From Trigger to copy the trigger setup for the selected search type to the search setup. For example, if the current trigger type is "Edge Trigger", clicking or tapping From Trigger copies the trigger settings to the "Edge" search setup.

**NOTE**

To use the "To Trigger" or "From Trigger" function, the current trigger type should correspond to the search type. Otherwise, a prompt message "Type mismatch" will pop up.

**4. Marktable On/Off**

Click or tap the MarkTable on/off switch to turn on or off the marktable display, as shown in the figure below. The table lists all events of the current waveform in the Waveform View. Zooming or adjusting the waveform causes the events in the table to change. You can perform the following operations on the table:

- When acquisitions are stopped (STOP mode), click or tap any row of the table to select the specified event. The inverted triangle mark of the selected event turns red like .

- Click or tap at the upper-right side of the table to open the search menu.

- Select the gray title bar of the table to drag the table and move the table window.

- Click or tap at the upper-right side of the table to close the search menu.
Figure 18.2 MarkTable Display

**5. Navigation**

Click or tap Navigation to access the navigation menu. You can use the "Search Event" mode in Navigation to navigate through the search events.

**6. Save search events**

You can save the event data to the instrument's internal memory or an external USB storage device in format of "*.csv".

Click or tap Save events to access the "Save" menu. For details, please refer to To Save a File.

## 18.2 Navigation

The Navigation function allows you to navigate time, search events, and segments. You can assess the Navigation menu in the following ways.

• Press the front-panel **Navigate** key to access the menu.

• Click or tap Navigate on the toolbar at the upper-right of the interface.

• In the "Search" menu, click or tap Navigation to access the menu.
Figure 18.3 Navigation Menu

The normal Navigation menu is as shown in the figure above. You can click or tap to minimize the menu (see the figure below) for a simplified interface.

Figure 18.4 Simplified Navigation Menu

**TIP**

The navigation function is available only when the oscilloscope is in "STOP" state (acquisition stopped).

**Navigate time**

It is available only when in "YT" time mode. The menu is as shown in Figure 18.3.

When "Time" is selected, click or tap in "Navigation" menu or press the front-panel key to start/stop playout. During playout, you can click or tap to play backward or to play forward. The playout automatically stops when it reaches the left or right edges. When it stops, clicking or tapping / moves the waveform. Click or tap the Speed drop-down button to select the speed level.

**Navigate search events**

After searching events using the Search function, you can select the "Search Event" mode in Navigation menu to navigate to specific events in the marktable. Its setting menu is as shown in Figure 18.5.
Figure 18.5 "Search Event" Navigation Setting Menu

After "Search Event" is selected, click or tap Search to open the "Search" menu and set the search condition. For search setup, please refer to Search. You can select the search type from the Type item. Click or tap to go to the previous search event or to go to the next search event. Click or tap to go to the first event or to go to the last event.

**Navigate segments**

This mode is available only in UltraAcquire acquisition mode. When UltraAcquire is enabled, the Mode is automatically set to "Frame Segment" which cannot be modified. Its setting menu is as shown in Figure 18.6.

Figure 18.6 "Frame Segment" Navigation Setting Menu

• In this mode, you can click or tap the Display mode drop-down button to set the display mode of segments. For details, please refer to UltraAcquire.

• Click or tap Start Frame and End Frame input fields to set the start frame and end frame which define the segment range to navigate through. You can also use the corresponding multipurpose knob to set the start/end frame. After you
click or tap the play/stop key, it plays from the "Start Frame" and the number of frames that can display on each screen page is (End Frame-Start Frame+1).

For example, if you set the start frame to 3 and the end frame to 9, it will play from the 3rd frame and displays 7 frames at a page.

• Click or tap in "Navigation" menu or press the front-panel key to start/ stop playing through the frames between the Start Frame and End Frame.

During playout, you can click or tap to play backward or to play forward. The playout automatically stops when it reaches the left or right edges. When it stops, you can click or tap / to go forward or backward. You can also click or tap to go to the first page or to go to the last page. The current page/total pages is indicated in Current Page.

**TIP**

During segment playing, you are not allowed to change the start/end frame.

# 19 Display Control

In the Display setting menu, you can set the type, persistence time, waveform intensity, grid type, grid brightness, and etc. Click or tap the function navigation icon at the lower-left corner of the screen, and then select Display to enter the "Display" menu. You can also click or tap the icon at the upper-right of the Waveform View to enter the "Display" menu.

Figure 19.1 Display Setting Menu

## 19.1 Display Type

This series oscilloscope provides the "Vector" display mode in which the sample points are connected by lines and displayed. In most cases, this mode can provide the most vivid waveform for you to view the steep edge of the waveform (such as square waveform).

## 19.2 Persistence Time

In the Display setting menu, click or tap the drop-down button of Persistence Time to select the persistence time. The available values are Min, specific values (100 ms, 200 ms, 500 ms, 1 s, 2 s, 5 s, 10 s), and Infinite.
In the following part, a frequency sweep signal of the sine waveform is used to show the waveform effects in different persistence times.

• **Min**
  Enables you to view waveform changing in high refresh rate.

• **Specific Values**
  Enables you to view glitches that change relatively slowly or glitches with lower occurrence probability. The persistence time can be set to 100 ms, 200 ms, 500 ms, 1 s, 2 s, 5 s, or 10 s.

• **Infinite**
  In this mode, the oscilloscope displays the waveform newly acquired without clearing the waveforms acquired formerly. The waveforms acquired formerly will be displayed in relatively low-brightness color and the newly acquired waveforms will be displayed in normal brightness and color. Infinite persistence can be used to measure noise and jitter and to capture incidental events.

## 19.3 Waveform Intensity

In Display menu, drag the slide bar of Wave Intensity to set the brightness of waveforms. The default is 50%, and the range available is from 1% to 100%.

## 19.4 To Set the Screen Grid

In the Display menu, select "FULL", "HALF", or "NONE" in Grid.

• **FULL**: turns the background grid on.

• **HALF**: turns part of the grid off, leaving only the main grid.

• **NONE**: turns the background grid off.

## 19.5 Display Settings

**Grid Brightness**

In the Display setting menu, drag the slider of Grid Brightness to set the grid brightness. The default is 50%, and the range available is from 0% to 100%.
**Window Transparency**

In the Display setting menu, drag the slider of Window Transparency to set the window transparency. The default is 50%, and the range available is from 0% to 100%.

**Cursor Brightness**

In the Display setting menu, drag the slider of Cursor Brightness to set the cursor brightness. The default is 80%, and the range available is from 0% to 100%.

## 19.6 Show Scale

In the Display setting menu, click or tap the Show Scale on/off switch to enable or disable scale display on the screen. By default, it is ON.

## 19.7 Color Grade

In the Display setting menu, click or tap the Color Grade on/off switch to enable or disable the color grade display. By default, it is OFF.

When it is enabled, different colors are displayed on the screen to indicate the times of data acquisition or acquisition probability.

## 19.8 Waveform Freeze

In the Display setting menu, click or tap the Waveform Freeze on/off switch to enable or disable the waveform freeze function. By default, it is ON.

When the function is enabled, the oscilloscope displays the waveform after multiple sampling and superposition when sampling is stopped. You can click or tap the STOP/RUN button at the upper-right side of the screen or press the front-panel key to stop sampling. If this function is disabled, the last triggered waveform is displayed.

# 20 Store and Load

You can save the setups, waveforms, screen image, and parameters of the current oscilloscope to the internal memory, an external USB storage device (such as USB flash drive), or an SMB shared folder in various formats and recall the stored setups or waveforms when necessary. You can also load the upgrade software to the system and perform the upgrade operation for the instrument.

You can also copy, delete, or rename the specified type of file from the internal memory, the external USB storage device, or the shared folder via the disk management menu.

This oscilloscope provides one USB HOST interfaces on the front panel, which can be connected to the USB storage device for external storage. The USB storage device connected is marked as "Removable USB Disk (D)".

## 20.1 To Enter the Storage Menu

You can enter the storage setting menu in the following ways.

• Click or tap the function navigation icon at the lower-left corner of the screen, and then select Storage to enter the storage setting menu.

• Click or tap the Storage button on the toolbar to enter the storage setting menu.

In the Storage setting menu, there are three sub-menus (Save, Load, and Upgrade) for you to choose. Select the specified sub-menu and configure the corresponding parameters.

## 20.2 To Save a File

In the Storage menu, click or tap the Save tab to enter the save setting menu. In this menu, you can save the image, waveform, or setup files.

### 20.2.1 To Save Image

In the Storage menu, click or tap the Save tab to enter the save operation menu. In this menu, click or tap the drop-down button of Choose to select "Save Image" to enter the "Save Image" setting menu. Set the relevant parameters and save the image to the internal or external memory.
Figure 20.1 Image Saving Setting Menu

**Set the image format**

• **Format**

Click or tap the drop-down button of Format to select "*.png", "*.bmp", or "*.jpg". Then the screen image will be saved to the internal or external memory in the selected format.

• **Invert**

Click or tap the Invert on/off switch to turn on/off inverting image colors.

• **Color**

Click or tap the Color toggle button to select "Color" or "Gray" images.

• **Header**

Click or tap the Header on/off switch to enable or disable the display of the header. If you select "ON", the instrument model and the image creation date will be displayed in the header of the image after you save the image file.

**Set the file saving parameters**

• **Set the filename**

Click or tap the input field of File Name to input the file name to be saved with the pop-up virtual keypad.

• **Set the file path**
Click or tap the input field of File Path, then the disk management interface is displayed. Select the target file path and then click or tap OK to set the file path. For detailed operations, refer to descriptions in Disk Management.

The default file path is "Local Disk". When a USB device is detected, the path is automatically set to "D:". When a shared folder is connected, the path is automatically set to "I:".

• **Overlay**

Click or tap the Overlay on/off switch to enable or disable the overwriting function. When this function is enabled, the existing file in the specified file path will be overwritten by the newly saved file that has the same filename as the existing one.

Click or tap Save, the current screen image is saved based on the settings and the storage menu is disabled.

**TIP**

When the quick action function is set to "Save Image" or "Save Group" with "Save Image" selected, you can press the front-panel **Quick** key to save the image.

### 20.2.2 To Save Wave

In the Storage menu, click or tap the Save tab to enter the save operation menu. In this menu, click or tap the drop-down button of Choose to select "Save Wave" to enter the "Save Wave" setting menu. The main settings (e.g. channel on/off state, vertical scale, and horizontal time base) and waveform data of all enabled channel will be saved to the internal or external memory.
Figure 20.2 Waveform Saving Setting Menu

**Set the source of the waveform data and the format of the saved waveform**

• **Data source**

Click or tap the drop-down button of Data Source to select "Screen" or "Memory".

• **Waveform format**

Click or tap the drop-down button of Format to select the format of the saved waveform. When the data source is set to "Screen", the format can be set to "*.bin" or "*.csv"; when the data source is set to "Memory", the format can be set to "*.bin", "*.csv", or "*.wfm".

**Set the file saving parameters**

• **Set the filename**

Click or tap the input field of File Name to input the file name to be saved with the pop-up virtual keypad.

• **Set the file path**

Click or tap the input field of File Path, then the disk management interface is displayed. Select the target file path and then click or tap OK. For detailed operations, refer to descriptions in Disk Management.
The default file path is "Local Disk". When a USB device is detected, the path is automatically set to "D:". When a shared folder is connected, the path is automatically set to "I:".

• **Overlay**

Click or tap the Overlay on/off switch to enable or disable the overwriting function. When this function is enabled, the existing file in the specified file path will be overwritten by the newly saved file that has the same filename as the existing one.

Click or tap Save, the current waveform file is saved based on the settings and the storage menu is disabled.

**TIP**

When the quick action function is set to "Save Wave" or "Save Group" with "Save Wave" selected, you can press the front-panel **Quick** key to save the waveform.

### 20.2.3 To Save Setup

In the Storage menu, click or tap the Save tab to enter the save operation menu. In this menu, click or tap the drop-down button of Choose to select "Save Setup" to enter the "Save Setup" setting menu. Save the settings of the oscilloscope to the internal or external memory in "*.stp" format. When loading, the stored settings can be recalled.

Figure 20.3 Setup Saving Setting Menu
**Set the file saving parameters**

• **Set the filename**

Click or tap the input field of File Name to input the file name to be saved with the pop-up virtual keypad.

• **Set the file path**

Click or tap the input field of File Path, then the disk management interface is displayed. Select the target file path and then click or tap OK. For detailed operations, refer to descriptions in Disk Management.

The default file path is "Local Disk". When a USB device is detected, the path is automatically set to "D:". When a shared folder is connected, the path is automatically set to "I:".

• **Overlay**

Click or tap the Overlay on/off switch to enable or disable the overwriting function. When this function is enabled, the existing file in the specified file path will be overwritten by the newly saved file that has the same filename as the existing one.

Click or tap Save, the current setup file is saved based on the settings and the storage menu is disabled.

**TIP**

When the quick action function is set to "Save Setup" or "Save Group" with "Save Setup" selected, you can press the front-panel **Quick** key to save the setup.

### 20.2.4 Binary Data Format (.bin)

Binary data format stores waveform data in binary format and provides data headers that describe these data. As data are displayed in binary format, its file size is much more smaller than that in ASCII format. If several channels are enabled, then all the displayed channels will be saved (save the first channel then save the second, and then it goes on like this until all the displayed channels are saved).

Table 20.1 BIN File Format

| File Header | Waveform Header | Waveform Data Header | Channel Data | Waveform Header | Waveform Data Header | Channel Data |
|-------------|-----------------|---------------------|--------------|-----------------|---------------------|--------------|
| 16 Bytes    | 140 Bytes       | 16 Bytes            | n Bytes      | 140 Bytes       | 16 Bytes            | n Bytes      |

In BIN file format, it contains the following channel data:

• CH1 Data
• CH2 Data
• CH3 Data
• CH4 Data
• Math Waveform Data

**Binary Header Format**

**1. File Header**

There is only one file header in a binary file. The file header contains the following information.

Table 20.2 File Header

| Cookie | Two-byte characters, RG, indicating that the file is the RIGOL binary data file format. |
|--------|-----------------------------------------------------------------------------|
| Version | Two-byte, indicating the file version. |
| File Size | An 8-byte long integer, indicating the number of bytes in the file. It includes the header. |
| Number of Waveforms | A 4-byte integer, indicating the number of waveforms that are stored in the file. |

**2. Waveform Header**

It is possible to store several waveforms in the file. Each stored waveform has a waveform header. When several channels are stored, each channel can be considered as a separate waveform. The waveform header contains the information about the type of waveform data that are stored following the waveform data header.

Table 20.3 Waveform Header

| Header Size | A 4-byte integer, indicating the number of bytes in the header. |
|-------------|-----------------------------------------------------------------------------|
| Waveform Type | A 4-byte integer, indicating the type of the waveform stored in the file. It is fixed to 1.<br>- 0 = Unknown<br>- 1 = Normal<br>- 2 = Peak Detection<br>- 3 = Average<br>- 4 = Not Used<br>- 5 = Not Used<br>- 6 = Logic |
| Number of Waveform Buffers | A 4-byte integer, indicating the number of waveform buffers required to read the data. It is fixed to 1. |
|----------------------------|-----------------------------------------------------------------------------|
| Number of Points | A 4-byte integer, indicating the number of waveform points in the data. |
| Count | A 4-byte integer. It is fixed to 0. |
| X Display Range | A 4-byte float, indicating the X-axis duration of the waveform that is displayed. For time-domain waveforms, it indicates the duration of the display. If the value is zero, then no data has been acquired. |
| X Display Origin | An 8-byte double-precision floating-point, indicating the X-axis value at the left edge of the screen. For time-domain waveforms, it indicates the time at the start of the display. The value is treated as a double precision 64-bit float point number. If the value is zero, then no data has been acquired. |
| X Increment | An 8-byte double-precision floating-point, indicating the duration between data points on the X-axis. For time-domain waveforms, it indicates the time between points. If the value is zero, then no data has been acquired. |
| X Origin | An 8-byte double-precision floating-point, indicating the X-axis value of the first data point in the data recording. For time-domain waveforms, it indicates the time of the first point. The value is treated as a double precision 64-bit float point number. If the value is zero, then no data has been acquired. |
| X Units | A 4-byte integer, indicating the unit of measurement for X values in the acquired data. It is fixed to 2.<br>- 0 = Unknown<br>- 1 = Volts (V)<br>- 2 = Seconds (s)<br>- 3 = Constant<br>- 4 = Amps (A)<br>- 5 = Decibel (dB)<br>- 6 = Hertz (Hz) |
| Y Units | A 4-byte integer, indicating the unit of measurement for Y values in the acquired data. The possible values are listed above under X Units. |
| Date | A 16-byte character array, indicating the date when the file is saved. |
| Time | A 16-byte character array, indicating the time when the file is saved. |
|------|-----------------------------------------------------------------------------|
| Model | A 24-byte character array in the format of MODEL#:SERIAL#, indicating the oscilloscope's model and serial number. |
| Channel Name | A 16-byte character array that contains the label assigned to the waveform. |

**3. Waveform Data Header**

A waveform may have multiple data sets. Each waveform data set has a waveform data header. The waveform data header consists of information about the waveform data set. The header is stored before the data set.

Table 20.4 Waveform Data Header

| Header Size | A 4-byte integer, indicating the number of bytes in the waveform data header. |
|-------------|-----------------------------------------------------------------------------|
| Buffer Type | A 2-byte integer, indicating the type of the waveform data stored in the file.<br>- 0 = Unknown<br>- 1 = Normal 32-bit float data<br>- 2 = Maximum float data<br>- 3 = Minimum float data<br>- 4 = Not Used<br>- 5 = Digital unsigned 8-bit character data (for digital channels) |
| Bytes Per Point | A 2-byte short integer, indicating the number of bytes per data point. |
| Buffer Size | An 8-byte long integer, indicating the number of bytes of the current channel waveform data. |

## 20.3 To Load a File

In the storage setting menu, click or tap the Load tab to switch to the load menu. In this menu, you can load the local file to the instrument.
Figure 20.4 Load Setting Menu

**Load Setup**

Click or tap the drop-down button of Choose to select "Load Setup". Then, click or tap File Path to select the internal memory (C:), external USB device (D:), or shared folder (I:) to load the settings. The default file type is "*.stp", and no other options are available. Select the file to be loaded from the memory. Click or tap Load to load the selected file.

## 20.4 Firmware Upgrade

This instrument supports local upgrade and online upgrade.

**Local upgrade**

1. In the storage setting menu, click or tap Upgrade to enter the local upgrade setting menu.
Figure 20.5 Upgrade Menu

2. Click or tap the input field of File Path, then the disk management interface is displayed. Select the upgrade file. For detailed operations, refer to Disk Management.

3. Click or tap Upgrade to complete the local upgrade.

**Online upgrade**

1. First ensure that the rear-panel LAN interface is connected to the network (if you have limited access to the Internet, please ask the administrator for permission).

2. Click or tap the function navigation icon at the lower-left corner of the screen to enter the function navigation.

3. Then click or tap the Upgrade icon to perform the upgrade operation.

## 20.5 Disk Management

You can enter the storage setting menu in the following ways.

• Click or tap the function navigation icon at the lower-left corner of the screen, and then select Storage to enter the storage setting menu.

• Click or tap the Storage button on the toolbar to enter the storage setting menu.

Then click or tap Disk at the lower-left corner of the "Storage" menu to enter the disk management interface, as shown in the figure below.
Figure 20.6 Disk Management Interface

Execute the following operations through the disk management menu:

**Select a Disk**

Before using the external storage device, make sure that a USB storage device (FAT32/NTFS format) is connected correctly.

By default, the "Local Disk(C)" is selected. After an external USB storage device (D:) or a shared folder (I:) is connected, you can select Removable USB Disk (D) or SMB (I) from the drop-down list at the upper-left corner of the "Disk" interface.

**Create a Folder**

Click or tap New Folder, then a folder name input keyboard is displayed.

For how to use the keypad, refer to descriptions in Parameter Setting Method. Click or tap any place on the screen to exit the keyboard.

**Clear the Internal Memory Safely**

Click or tap SecurityClear, then a prompt message "Execute secure memory wipe?" is displayed. Click or tap OK to clear all the files stored in the internal disk. Otherwise, click or tap Cancel to cancel security clear operation.

**Select a File**

Before operating on the file or folder, first select the desired file or folder.

Click or tap the check box at the right side of the folder, if checked, it is selected, with an icon being displayed. Click or tap the check box again or to deselect it. The check box restores its original state.
This series supports selecting multiple files or folders to operate on. You can also click or tap the icon at the upper-right corner of the interface to select all the files and folders under the current disk. Click or tap to cancel the select-all operation.

**Cut, Copy, or Paste a File or a Folder**

• **Cut a File to a Specified Folder**

Select a specified file or folder. Click or tap Cut to cut the specified file or folder. Then select the destination folder. Then click or tap Paste to paste the specified file or folder to the destination folder.

• **Copy a File to a Specified Folder**

Select a specified file or folder. Click or tap Copy to copy the specified file or folder. Then select the destination folder. Then click or tap Paste to paste the specified file or folder to the destination folder.

**Delete a File or Folder**

In the current folder, select the file or folder to be deleted. Click or tap Delete, then a prompt message "Are you sure to delete the file?" is displayed. Click or tap OK to delete the file. Otherwise, click or tap Cancel to cancel the deletion operation.

**Rename a File or Folder**

Select a specified file or folder, then click or tap Rename to input a new filename or folder name with the pop-up virtual keypad. Then, the rename operation is completed.

## 20.6 SMB Configuration

In the storage setting menu, click or tap SMB Setting to enter the SMB setting menu. In this menu, you can configure SMB to connect the instrument to your PC and share files.
Figure 20.7 SMB Setting Menu

**Operation Procedures**

Take Windows 10 Pro as an example. Follow the steps below to use SMB to share files.

1. **Enable the SMB file sharing function in the computer.**

   a. Open the Control Panel and click **Programs and Features**.

   b. Click **Turn Windows features on or off**.
c. In the pop-up window, find the SMB 1.0/CIFS File Sharing Support option. Check all the check boxes for this option and select OK.

d. Restart the computer and then the SMB file sharing function is enabled.

2. Create a shared folder.

a. Create a new folder (containing English characters only). Right-click the folder and select Give access to > Specific People.
b. In the pop-up window, select a specific user or "Everyone" and click **Add**. Then you can set the permission level.

c. Click **Share** > **Done** to complete the creation of a shared folder.

3. Configure the instrument.

a. In the storage setting menu, click or tap **SMB Setting** to enter the SMB setting menu. You can set the server path, user name, and password.

**NOTE**

- The server path format is \\xxx.xxx.xxx.xxx\name, where "xxx.xxx.xxx.xxx" is the IP address and "name" is the name of the shared folder. For example, the server path can be \\172.16.25.77\DHOShare.

- You can press Windows key + R to open the Run window. Enter "netplwiz" and click OK to check the user account. The user name and the password are case sensitive.

b. Click or tap Connect to connect the instrument to the computer. Then "Connect" is displayed for the Connect State item in the SMB setting menu.

You can also turn on Boot Auto_Connect. In this case, the instrument is automatically connected to the computer according to the server path, user name, and password settings upon the next power-on.

**Share the File**

After the SMB server is connected, you can access and manage the contents of the shared folder through your PC and the oscilloscope's disk management system.

The shared folder is displayed as "SMB (I)" in the oscilloscope. Click or tap the dropdown menu at the upper-left of the disk management interface to select "SMB (I)" to open the shared folder. The management method of shared files is identical to that of disk C and disk D (refer to Disk Management).
**TIP**

You can also save files to the shared folder through the oscilloscope. In the save setting menu, set the file path to "SMB (I)" and then save the file.

# 21 System Utility Function Setting

In the Utility menu, you can set the I/O parameters and the system-related function parameters. You can enter the "Utility" menu in the following ways.

• Click or tap the Notification Area at the lower-right corner of the screen. Then the Utility menu is displayed.

• Click or tap > Utility to enter the Utility menu.

## 21.1 I/O Setting

In Utility menu, click or tap IO to enter the I/O setting menu to configure the following parameters.

**Network Status**

Different prompts will be displayed according to the current network connection status.

• Network Config Succeeded!

• Acquiring IP...
• IP Conflict!

• DISCONNECTED
• DHCP Config Failed
• Read Status Fail!

• CONNECTED
• Invalid IP
• IP lost
• Please wait...

**MAC Address**

For each instrument, the MAC address is unique. When assigning the IP address for the instrument, the system uses the MAC address to identify the instrument.

**VISA Address**

Displays the VISA address currently used by the instrument.
**IP Configuration Type**

The configuration type of the IP address can be DHCP, Auto IP, or Static IP. In different IP configuration types, the configurations for IP address and other network parameters are different.

• **DHCP**

If "DHCP" is selected, the DHCP server in the current network will assign the network parameters (e.g. IP address, Subnet, Gateway, and DNS) for the instrument.

• **Auto IP**

When "Auto IP" is selected, the instrument will acquire the IP address ranging from "169.254.0.1" to "169.254.255.254" and the subnet mask (255.255.0.0) automatically based on the current network configuration. The "Auto IP" works only when "DHCP" is not selected or the connection failed.

• **Static IP**

If "Static IP" is selected, the instrument is configured with static IP. In this case, you need to disable DHCP and Auto IP manually. Then you need to configure the parameters such as "IP address", "Subnet", "Gateway", and "DNS" manually. At this time, you can self-define the network parameters (e.g. IP address) of the instrument.

- **Set the IP address**

The format of the IP address is nnn.nnn.nnn.nnn. The range of the first segment (nnn) of the address is from 0 to 255 (except 127); wherein, the valid range is from 0 to 223. The range for the other three segments is from 0 to 255. You are recommended to ask your network administrator for an IP address available.

This setting will be saved to the non-volatile memory; if "Load Last" is set to "Last", then DHCP and Auto IP are disabled at the next power-on. The instrument will load the preset IP address automatically.

- **Set the subnet mask**

The format of the subnet mask is nnn.nnn.nnn.nnn. Wherein, the range of "nnn" is from 0 to 255. You are recommended to ask your network administrator for a subnet mask available.

This setting will be saved in the non-volatile memory; if "Load Last" is set to "Last", then DHCP and Auto IP are disabled at the next power-on. The instrument will load the preset subnet mask automatically.

- **Set the default gateway**

You can set this parameter in Static IP mode. The format of the gateway is nnn.nnn.nnn.nnn. The range of the first segment (nnn) is from 0 to 223 (except 127), and the range for the other three segments is from 0 to 255.
You are recommended to ask your network administrator for a gateway address available.

This setting will be saved in the non-volatile memory; if "Load Last" is set to "Last", then DHCP and Auto IP are disabled at the next power-on. The instrument will load the preset gateway automatically

- **Set the DNS address**

You can set this parameter in Static IP mode. The format of the DNS address is "nnn.nnn.nnn.nnn". The range for the first segment (nnn) of the address is from 0 to 223 (except 127); and the range for the other three segments is from 0 to 255. You are recommended to ask your network administrator for an address available.

Generally, you do not need to set the DNS, so this parameter setting can be ignored.

**TIP**

• When the three IP configuration types are all turned on, the priority of the parameter configuration from high to low is "DHCP", "Auto IP", and "Static IP".

• The three IP configuration types cannot be all turned off at the same time.

**mDNS**

Click or tap the mDNS on/off switch to enable or disable the multicast Domain Name System (mDNS). This system is used to provide the function of DNS server for service discovery in a small network without a DNS server.

**Host Name**

A maximum of 26-byte strings can be supported.

**Apply the Network Parameter Setting**

Drag the menu up on the screen. Click or tap Apply at the bottom to validate the current network parameter setting.

## 21.2 Basic Settings

In the Utility menu, click or tap Setup to enter the basic setting menu.

**Language**

This product supports menus in multiple languages, including the display of the help information, prompt messages, and interface. Click or tap the drop-down button of Language to select the specified system language.

**Load Last**

You can set the system configuration to be recalled when the oscilloscope is powered on again after power-off. Click or tap "Default" or "Last" for Load last.
• Last: returns to the setting of the system at last power-off.

• Default: returns to the factory setting of the system.

**Power Status**

• Switch Off: After the oscilloscope is connected to power, you need to press the power key on the front panel to power on the instrument.

• Switch On: After the oscilloscope is connected to power, it will be powered on immediately.

**Beeper**

Click or tap the Beeper on/off switch to enable or disable the beeper. When the beeper is enabled, you can hear the beeper sound in the following situations:

• Use a front-panel key or a menu key
• Use the touch screen
• When a prompt message is displayed

**AUX Output**

You can set the type of the signal output from the [AUX OUT] connector on the rear panel.

• TrigOut: After this type is selected, at each trigger (hardware trigger), the oscilloscope outputs a signal from the [AUX OUT] connector on the rear panel that can reflect the current capture rate of the oscilloscope. If this signal is connected to a waveform display device to measure the frequency, the found measurement result is the same as the current capture rate.

• PassFail: When this type is selected, the instrument can output a positive or negative pulse via the [AUX OUT] connector when a successful or failed event is detected. Refer to descriptions in To Set the Output Form of the Test Results.

Enabling the Aux Output function in "PassFail" menu automatically toggles the AUX Out parameter to "PassFail"; setting the AUX Out parameter to "TrigOut" automatically disables the Aux Output function in "PassFail" menu.

**Input Lock**

Once the input lock is enabled, the input function is disabled, for which you can no longer use the touch screen, front-panel keys, and knobs to configure the instrument.

Press the front-panel channel keys in the order of **1**, **1**, **2**, **2** to disable the input lock.
**Expand**

The waveform display can be set to expand or compress about the "Center" or "GND".

• Center: When the vertical scale is changed, the displayed waveform will expand or compress about the center of the display.

• GND: When the vertical scale is changed, the displayed waveform will expand or compress about the ground level position of the signal.

**Fine/Zoom**

It sets the effect of pressing the front-panel Horizontal **SCALE** knob.

• Fine: enables or disables the fine adjustment when the knob is pressed.

• Zoom: enables or disables the Zoom mode when the knob is pressed.

## 21.3 About this Oscilloscope

In Utility menu, click or tap About, and then you can view the model, version, and other information about this instrument in About menu.

• **Model**
  Indicates the product model.

• **Serial Number**
  Indicates the serial number, the unique identification for the product.

• **Firmware**
  Indicates the firmware version number of the product.

• **Hardware**
  Indicates the hardware version number of the product.

• **Build**
  Indicates the creation time of the software version.

• **Android.Build**
  Indicates the creation time of the Android operating system.

• **Android.Version**
  Indicates the version number of the Android operating system. For example, 7.1.0.

• **Launcher**
  Indicates the desktop UI version number of the Android operating system.
• WebControl
  Indicates the version number of browser remote control module.

## 21.4 Other Settings

**Open Source Acknowledgment**

Click or tap Open Source Acknowledgment to view the open source acknowledgment of this series oscilloscope in the pop-up window.

## 21.5 Auto Config

In "Utility" menu, click or tap Auto Config to enter the menu in which you can configure the Auto function.

• Click or tap Peak to Peak on/off switch to enable or disable the peak-to-peak priority setting. This function is intended for the shifted signal. If there is a large deviation, you can view the signal waveform in priority when you enable the function.

• Click or tap Live CH on/off switch to turn on/off examining channels that are turned on.

If "OFF" is selected, enable the Auto function and 4 analog channels (CH1-CH4) will be examined for signal activity in sequence. If no signal is detected for a specified channel, the channel will be turned off; otherwise, if a signal is detected, the channel will be autoscaled to best display the signal. If "ON" is selected, enable the Auto function and only the channels that are turned on will be examined.

• Click or tap Overlay on/off switch to enable or disable the waveform overlay display function. If enabled, waveforms of different channels will be displayed in the same position of the screen; if disabled, waveforms of different channels will be displayed on the screen from top to bottom in sequence.

• Click or tap Keep Coupling on/off switch to turn on/off maintaining channel coupling. If "ON" is selected, enable the Auto function and the channel coupling setting is maintained; if "OFF" is selected, the channel coupling is DC coupling by default.
## 21.6 SelfCal

The self-calibration program can quickly make the oscilloscope to work in an optimal state to get the precise measurement results. You can perform self-calibration at any time, especially when the changes of the ambient temperature reach or exceed 5℃.

Make sure that the oscilloscope has been warmed up or operating for more than 30 minutes before the self-calibration.

In "Utility" menu, click or tap SelfCal, the self-calibration menu is as shown below.

Figure 21.1 Self-calibration Menu

• Click or tap Start, and then the oscilloscope will start to execute the self-calibration program.

• After starting the self-calibration program, click or tap Exit to cancel self-calibration operation at any time.

• Click or tap Close to close the self-calibration information window.

## 21.7 Option List

In the "Utility" menu, click or tap Options to view all the options of the instrument.

## 21.8 Quick Action Settings

In Utility menu, click or tap Quick to enter the menu to configure the quick action key on the front panel.
Figure 21.2 Quick Menu

**Save Image**

• Click or tap Save Image, then Operation is set to "Save Image".

• In the Format menu item, available image types include "png", "bmp", and "jpg".

• Click or tap the Invert on/off switch to turn on/off inverting image colors.

• Click or tap "Color" or "Gray" for Color to select the desired image color.

After setup, click or tap the **Quick** key at the upper-right corner of the front panel to capture the current screen and save the image with the specified format. The location where the file is saved depends on the File Path setting in Storage menu. For details, please refer to To Save a File.

**Save Wave**

• Click or tap Save Wave, then Operation is set to "Save Wave".

• Select "Memory" or "Screen" under Data Source as the source of the saved waveform.

• Available options under Format include "bin" and "csv".
After setup, click or tap the **Quick** key at the upper-right corner of the front panel to save the waveform based on the settings. The location where the file is saved depends on the File Path setting in Storage menu. For details, please refer to To Save a File.

**Save Setup**

Click or tap Save Setup, then Operation is set to "Save Setup".

After setup, click or tap the **Quick** key at the upper-right corner of the front panel to save the setup file suffixed with ".stp". The location where the file is saved depends on the File Path setting in Storage menu. For details, please refer to To Save a File.

**All Measurements**

• Click or tap All Measure, then Operation is set to "All Measure".

• In All Measure item, click or tap the drop-down button to select the channel (CH1-CH4) to measure.

After setup, click or tap the **Quick** key at the upper-right corner of the front panel to perform the measurement on the specified channel.

**Reset Statistics**

• Click or tap Stat Reset, then Operation is set to "Stat Reset".

• Click or tap "Measure" or "Pass/Fail" under Stat Reset to reset all statistics of the "Measure" or "Pass/Fail" function.

After setup, click or tap the **Quick** key at the upper-right corner of the front panel. This resets all statistics of the specified function in the Result sidebar at the right side of the screen and starts the measurements again.

**Waveform Recording**

Click or tap Record, then Operation is set to "Record".

After setup, click or tap the **Quick** key at the upper-right corner of the front panel to perform the waveform recording.

**Save Group**

• Click or tap Save Group, then Operation is set to "Save Group".

• Under Save Group, select one or more items from "Save Image", "Save Wave", and "Save Setup".
After setup, click or tap the **Quick** key at the upper-right corner of the front panel to save the selected items based on the settings. The location where the file is saved depends on the File Path setting in Storage menu. For details, please refer to To Save a File.

## 21.9 Self-check

In Utility menu, click or tap Self Check to enter the "Self Check" setting. You can test the following self-check items for the device.

**Key Test**

Click or tap Key Test to enter the key test interface (virtual front-panel key).

At this time, you can press the front-panel keys to check whether the virtual keys are highlighted. If yes, it indicates that the keys work normally; if no, it indicates that there's something wrong with the keys. Click or tap Exit at the lower-left corner of the interface to exit the key test interface.

**Touch Test**

Click or tap Touch Test to enter the touch screen test interface.

Slide with your finger on the screen. If there is a line displaying at the empty area where you slide on the screen and the box that you tap turns out to be filled with green background, it indicates that the touch function of this area is normal. Click or tap Exit at the lower-left corner of the interface to exit the touch screen test interface.

**Screen Test**

Click or tap Screen Test to enter the screen test interface and check whether the defective pixel exists.

There are 15 screen test interfaces. Click or tap the screen to switch to the next screen test interface. Click or tap Exit at the upper-left corner of the interface to exit the screen test interface.

**Board Test**

Click or tap Board Test, then the board test interface is displayed. Check whether the status of each module is in good condition.

# 22 Remote Control

The following ways of remote control are supported:

• **User-defined Programming**

Users can program and control the instrument by using the SCPI (Standard Commands for Programmable Instruments) commands. For details about the SCPI commands and programming, refer to Programming Guide of this product series.

• **PC Software**

You can use the PC software to send SCPI commands to control the instrument remotely. RIGOL Ultra Sigma is recommended. You can download the software from RIGOL official website (http://www.rigol.com).

Operation Procedures:
- Set up communication between the instrument and PC.
- Run Ultra Sigma and search for the instrument resource.
- Open the remote command control panel to send commands.

• **Web Control**

This instrument supports Web Control. Connect the instrument to the network, then input the IP address of the instrument into the address bar of the browser of your computer. The web control interface is displayed. Click Web Control to enter the web control page. Then you can view the display of the real-time interface of the instrument. Through the Web Control method, you can migrant the device control to the control terminals (e.g. PC, Mobile, iPad, and other smart terminals) to realize remote control of the instrument. You have to log in before using the Web Control to modify network settings. When you first log in to the Web Control, the user name is "admin" and password is "rigol".

This instrument can be connected to the PC via the USB and LAN interface to set up communication and realize remote control through the PC.

This chapter will illustrate how to use the RIGOL Ultra Sigma software to remotely control the instrument via various interfaces.

**CAUTION**

Before connecting the communication cable, please turn off the instrument to avoid causing damage to the communication interfaces.
## 22.1 Remote Control via USB

1. **Connect the device**

Use the USB cable to connect the rear-panel USB DEVICE interface of the instrument to the USB HOST interface of the PC.

2. **Search for the device resource**

Start up Ultra Sigma and the software will automatically search for the resource currently connected to the PC via the USB interface. You can also click USB-TMC to search for the resource.

3. **View the device resource**

The resources found will appear under the "RIGOL Online Resource" directory, and the model number and USB interface information of the instrument will also be displayed.

4. **Control the instrument remotely**

Right-click the device resource name and select "SCPI Panel Control" to open the remotely command control panel. Then you can send commands and read data through the panel. For details about the SCPI commands and programming, refer to the Programming Guide of this instrument.

## 22.2 Remote Control via LAN

1. **Connect the device**

Use the network cable to connect the instrument to your local area network (LAN).

2. **Configure network parameters**

Configure the network parameters of the instrument in Utility>IO menu.

3. **Search for Search device resource**

Start up Ultra Sigma and click LAN to open the panel as shown in the figure below. Click Search and the software searches for the instrument resources currently connected to the LAN and the resources found are displayed at the right section of the window as shown in the figure below. Click OK to add it.
Besides, you can input the IP address of the instrument manually into the text field under "Manual Input LAN Instrument IP", then click TEST. If the instrument passes the test, click Add to add the instrument to the LAN instrument resource list in the right section; if the instrument fails the test, please check whether the IP address that you input is correct, or use the auto search method to add the instrument resource.

4. View the device resource

The resources found will appear under the "RIGOL Online Resource" directory.

5. Control the instrument remotely

Right-click the device resource name and select "SCPI Panel Control" to open the remotely command control panel. Then you can send commands and read data through the panel.

6. Load LXI webpage

As this instrument conforms to LXI CORE 2011 DEVICE standards, you can load LXI web page through Ultra Sigma (right-click the instrument resource name and select "LXI-Web"). Various important information about the instrument (including the model, manufacturer, serial number, description, MAC address, and IP address) will be displayed on the web page. You can also directly input the IP address of the instrument in the address bar of the PC browser to load the LXI web page.
# 23 Troubleshooting

1. When I power on the instrument, the instrument's screen stays black and does not display anything.

   a. Check whether the power supply has been connected correctly.

   b. Check whether the power key is really pressed.

   c. Restart the instrument after finishing the above inspections.

   d. If the problem still persists, please contact RIGOL.

2. No waveform of the signal is displayed on the screen.

   a. Check whether the probe is properly connected to the item under test.

   b. Check whether there are signals generated from the item to be tested (you can connect the probe compensation output signal to the faulty channel to locate the problem, and then determine whether the channel or the item to be tested has a problem).

   c. Resample the signal.

   d. If the problem still persists, please contact RIGOL.

3. The USB storage device cannot be recognized.

   a. Check whether the USB storage device can work normally when connected to other instruments or PC.

   b. Make sure that the USB storage device is FAT32/NTFS format. The instrument doesn't support hardware USB storage device.

   c. After restarting the instrument, insert the USB storage device again to check whether it can work normally.

   d. If the USB storage device still cannot work normally, please contact RIGOL.

4. The touch-enabled operation does not work.

   a. Check whether you have locked the touch screen. If yes, unlock the touch screen.

   b. Check whether the screen or your finger is stained with oil or sweat. If yes, please clean the screen or dry your hands.

   c. Check whether there is a strong magnetic field around the instrument. If the instrument is close to the strong magnetic field (e.g. a magnet), please move the instrument away from the magnet field.

   d. If the problem still persists, please contact RIGOL.

# 24 Appendix

## 24.1 Appendix A: Options and Accessories

| Order Information | Order No. |
|-------------------|-----------|
| **Model** | |
| 100 MHz, 1.25 GSa/s, 25 Mpts, 4CH | DHO814 |
| 100 MHz, 1.25 GSa/s, 25 Mpts, 2CH | DHO812 |
| 70 MHz, 1.25 GSa/s, 25 Mpts, 4CH | DHO804 |
| 70 MHz, 1.25 GSa/s, 25 Mpts, 2CH | DHO802 |
| **Standard Accessories** | |
| Power Adaptor Conforming to the Standard of the Destination Country | — — |
| Banana-Plug Ground Connecting Cable | — — |
| DHO814/DHO804: Passive Probe x4 (150 MHz)<br>DHO812/DHO802: Passive Probe x2 (150 MHz) | PVP3150 |

**NOTE**

For all the mainframes, accessories and options, please contact the local office of RIGOL.

## 24.2 Appendix B: Warranty

RIGOL TECHNOLOGIES CO., LTD. (hereinafter referred to as RIGOL) warrants that the product mainframe and product accessories will be free from defects in materials and workmanship within the warranty period. If a product proves defective within the warranty period, RIGOL guarantees free replacement or repair for the defective product.

To get repair service, please contact your nearest RIGOL sales or service office.

There is no other warranty, expressed or implied, except such as is expressly set forth herein or other applicable warranty card. There is no implied warranty of merchantability or fitness for a particular purpose. Under no circumstances shall RIGOL be liable for any consequential, indirect, ensuing, or special damages for any breach of warranty in any case.

## 24.3 Appendix C: Factory Settings

Press the front-panel **DEFAULT** or click/tap Default on the Toolbar and a prompt message "Restore default settings?" is displayed. Click or tap OK to restore the instrument to its factory default settings, as shown in the table below.

Table 24.2 Factory Settings

| Parameter | Factory Settings |
|-----------|------------------|
| **Horizontal** | |
| Horizontal Time Base | 2 μs |
| Horizontal Position | 0 s |
| Delayed Sweep | OFF |
| Roll | Auto |
| Fine | OFF |
| Horizontal Expansion | Center |
| **Acquisition** | |
| Acquisition Mode | Normal |
| Memory Depth | 10 kpts |
| **Vertical** | |
| CH1 On/Off | ON |
| CH2 On/Off | OFF |
| CH3 On/Off | OFF |
| CH4 On/Off | OFF |
| Impedance | 1 MΩ |
| Fine | OFF |
| Vertical Scale | 50 mV |
| Vertical Offset | 0 V |
| Channel Unit | [V] |
| Channel Coupling | DC |
| Bias | 0 V |
| BW Limit | OFF |
| Channel Delay | 0 s |
| Display Label | OFF |
| Invert | OFF |
| Attenuation | 1X |
| **Trigger** | |
| Trigger Type | Edge Trigger |
| Trigger Mode | Auto |
| Parameter | Factory Settings |
|-----------|------------------|
| Source Selection | CH1 |
| Edge Type | Rising |
| Trigger Coupling | DC |
| Trigger Holdoff | 8 ns |
| Noise Rejection | OFF |
| **Display** | |
| Display Type | Vector |
| Persistence Time | Min |
| Waveform Intensity | 50% |
| Grid | FULL |
| Grid Brightness | 50% |
| Window Transparency | 50% |
| Cursor Brightness | 80% |
| Show Scale | ON |
| Color Grade | OFF |
| Waveform Freeze | ON |
| **Measure** | |
| Threshold | OFF |
| Indicator | OFF |
| Histogram | OFF |
| Statistics | OFF |
| Count | 1,000 |
| Display Type | % |
| Source | CH1 |
| Upper | 90% |
| Mid | 50% |
| Lower | 10% |
| Amplitude Measurement Method | Auto |
| Region | Main |
| **Cursor** | |
| Mode | OFF |
| **Manual** | |
| Source | CH1 |
| Select | X |
| AX BX | OFF |
| AY | -6 μs |
| BY | 6 μs |
| **Track** | |
| Parameter | Factory Settings |
|-----------|------------------|
| AX Source | CH1 |
| BX Source | CH1 |
| AX BX | OFF |
| Track | X |
| AX | -6 μs |
| BX | 6 μs |
| **XY** | |
| Select | X |
| AX BX | OFF |
| AX | -150 mV |
| BX | 150 mV |
| **Frequency Counter** | |
| Source | CH1 |
| Statistics | OFF |
| Measure | Frequency |
| Resolution | 4 |
| **DVM** | |
| Source | CH1 |
| Mode | AC RMS |
| Beeper | OFF |
| Limits Condition Setting | In Limits |
| Upper | 1 V |
| Lower | 0 V |
| **Save Image** | |
| Format | *.png |
| Invert | OFF |
| Color | Color |
| Header | ON |
| Overlay | OFF |
| **Save Wave** | |
| Data source | Screen |
| Format | *.bin |
| **Save Setup** | |
| File Type | *.stp |
| **Load Setup** | |
| File Type | *.stp |
| Parameter | Factory Settings |
|-----------|------------------|
| **System Setting** | |
| Beeper | OFF |
| AUX Output | TrigOut |
| Input Lock | OFF |
| Expand | GND |
| Fine/Zoom | Fine |
| **Auto Config** | |
| Peak to Peak | ON |
| Live CH | OFF |
| Overlay | ON |
| Coupling | OFF |
| **Quick Settings** | |
| Operation | Save Image |
| Format | *.png |
| Invert | OFF |
| Color | Color |
| **Pass/Fail Test** | |
| Enable | OFF |
| Source | CH1 |
| Y Mask | 480 mdiv |
| X Mask | 240 mdiv |
| Format (to load file) | *.pf |
| Format (to save file) | *.pf |
| File Name | RigolDS |
| Aux Output | OFF |
| Pulse | 1 μs |
| Output Event | Fail |
| Polarity | Positive |
| Error Action | Stop |
| **Waveform Recording** | |
| Waveform Recording | OFF |
| **Record** | |
| Interval | 10 ns |
| Frames | 1,000 |
| Beeper | 🔊 |
| **Play** | |
| Minimize | OFF |
| Play Mode | ▶️ |
| Parameter | Factory Settings |
|-----------|------------------|
| Play Sequence | ▶ |
| Interval | 100 ms |
| **Math Operation** | |
| Invert | OFF |
| Expand | GND |
| Display Label | OFF |
| Grid | FULL |
| **A+B** | |
| Operation | OFF |
| Source A | CH1 |
| Source B | CH1 |
| Scale | 500 mV |
| Offset | 0 V |
| **A-B** | |
| Operation | OFF |
| Source A | CH1 |
| Source B | CH1 |
| Scale | 500 mV |
| Offset | 0 V |
| **A×B** | |
| Operation | OFF |
| Source A | CH1 |
| Source B | CH1 |
| Scale | 500 mU |
| Offset | 0 U |
| **A÷B** | |
| Operation | OFF |
| Source A | CH1 |
| Source B | CH1 |
| Scale | 500 mU |
| Offset | 0 U |
| **FFT** | |
| Operation | OFF |
| Source | CH1 |
| X | Span-Center |
| Unit | dBm/dBV |
| Center Frequency | 5 MHz |
| Frequency Range | 10 MHz |
| Vertical Scale | 20 dB |
| Offset | 0 dBV |
| Parameter | Factory Settings |
|-----------|------------------|
| Window Function | Hanning |
| Color Grade | OFF |
| Peak Search | OFF |
| Peak Number | 5 |
| Threshold | 5.5 dBV |
| Threshold | 1.8 dB |
| Order | Amp Order |
| **A&&B** | |
| Operation | OFF |
| Source A | CH1 |
| Source B | CH1 |
| Waveform Size | Medium |
| Offset | 0 div |
| Sensitivity | 300 mdiv |
| Thre.CH1 | 0 V |
| Thre.CH2 | 0 V |
| Thre.CH3 | 0 V |
| Thre.CH4 | 0 V |
| **A\|\|B** | |
| Operation | OFF |
| Source A | CH1 |
| Source B | CH1 |
| Waveform Size | Medium |
| Offset | 0 div |
| Sensitivity | 300 mdiv |
| Thre.CH1 | 0 V |
| Thre.CH2 | 0 V |
| Thre.CH3 | 0 V |
| Thre.CH4 | 0 V |
| **A^B** | |
| Operation | OFF |
| Source A | CH1 |
| Source B | CH1 |
| Waveform Size | Medium |
| Offset | 0 div |
| Sensitivity | 300 mdiv |
| Thre.CH1 | 0 V |
| Thre.CH2 | 0 V |
| Thre.CH3 | 0 V |
| Thre.CH4 | 0 V |
| **!A** | |
| Parameter | Factory Settings |
|-----------|------------------|
| Operation | OFF |
| Source A | CH1 |
| Waveform Size | Medium |
| Offset | 0 div |
| Sensitivity | 300 mdiv |
| Thre.CH1 | 0 V |
| Thre.CH2 | 0 V |
| Thre.CH3 | 0 V |
| Thre.CH4 | 0 V |
| **Intg** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mV*s |
| Offset | 0 V*s |
| Offset | 0 V |
| **Diff** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mV/s |
| Offset | 0 V/s |
| Smooth | 5 |
| **Sqrt** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mU |
| Offset | 0 U |
| **Lg** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mU |
| Offset | 0 U |
| **Ln** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mU |
| Offset | 0 U |
| **Exp** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mU |
| Offset | 0 U |
| Parameter | Factory Settings |
|-----------|------------------|
| **Abs** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mV |
| Offset | 0 V |
| **Low Pass** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mV |
| Offset | 0 V |
| ωc | 20 MHz |
| **High Pass** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mV |
| Offset | 0 V |
| ωc | 20 MHz |
| **Band Pass** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mV |
| Offset | 0 V |
| ωc1 | 20 MHz |
| ωc2 | 40 MHz |
| **Band Stop** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mV |
| Offset | 0 V |
| ωc1 | 20 MHz |
| ωc2 | 40 MHz |
| **AX+B** | |
| Operation | OFF |
| Source | CH1 |
| Scale | 500 mV |
| Offset | 0 V |
| A | 1 |
| B | 0 |
| **Ref** | |
| Current | Ref1 |
| Source | CH1 |
| Parameter | Factory Settings |
|-----------|------------------|
| Vertical Scale | 50 mV |
| Vertical Offset | 0 V |
| Label | REF1 |
| Label Display | OFF |
| Color | Orange |
| **Decode** | |
| Bus Type | Parallel |
| Bus Status | OFF |
| Format | Hex |
| Label | ON |
| Event Table | OFF |
| **Parallel** | |
| CLK | OFF |
| Bus | CH1 |
| Threshold | 0 V |
| Endian | Invert |
| Polarity | Positive |
| **RS232** | |
| TX | CH1 |
| RX | OFF |
| Threshold | 0 V |
| Polarity | Positive |
| Baud Rate | 9.6 kbps |
| Data | 8 bits |
| Endian | LSB |
| Parity | None |
| Stop Bit | 1 bit |
| **I2C** | |
| CLK | CH1 |
| SCL Thre | 0 V |
| Data | CH2 |
| SDA Thre | 0 V |
| Exchange | SCL/SDA |
| R/W | Without |
| **SPI** | |
| CLK | CH1 |
| CLK Threshold | 0 V |
| Edge Type | Rising |
| MISO | CH2 |
| MISO Threshold | 0 V |
| MOSI | OFF |
| Parameter | Factory Settings |
|-----------|------------------|
| Mode | CS |
| CS | CH3 |
| CS Threshold | 0 V |
| CS Polarity | Negative |
| Polarity | Positive |
| Width | 8 |
| Endian | MSB |
| **CAN** | |
| Source | CH1 |
| Threshold | 0 V |
| Signal Type | CAN_H |
| Baud | 1 Mbps |
| Sample Position | 50% |
| **Histogram Analysis** | |
| Enable | OFF |
| Type | Horizontal |
| Source | CH1 |
| Height | 2 div |
| Left Limit | -4 μs |
| Right Limit | 4 μs |
| Top Limit | 100 mV |
| Bottom Limit | -50 mV |

**Boost Smart World and Technology Innovation**

Industrial Intelligent Manufacturing | Semiconductors  
Education & Research | Communication  
System Integration | New Energy

**Technology Areas:**
- Cellular-5G/WIFI
- UWB/RFID/ZIGBEE
- Digital Bus/Ethernet
- Optical Communication

- Digital/Analog/RF Chip
- Memory and MCU Chip
- Third-Generation Semiconductor
- Solar Photovoltaic Cells

- New Energy Automobile
- PV/Inverter
- Power Test
- Automotive Electronics

**Provide Testing and Measuring Products and Solutions for Industry Customers**

---

## Contact Information

**HEADQUARTER**  
RIGOL TECHNOLOGIES CO., LTD.  
No.8 Keling Road, New District,  
Suzhou, JiangSu, P.R.China  
Tel: +86-400620002  
Email: info-cn@rigol.com

**EUROPE**  
RIGOL TECHNOLOGIES EU GmbH  
Carl-Benz-Str.11  
82205 Gilching  
Germany  
Tel: +49(0)8105-27292-0  
Email: info-europe@rigol.com

**NORTH AMERICA**  
RIGOL TECHNOLOGIES, USA INC.  
10220 SW Nimbus Ave.  
Suite K-7  
Portland, OR 97223  
Tel: +1-877-4-RIGOL-1  
Email: sales@rigol.com

**JAPAN**  
RIGOL JAPAN CO., LTD.  
5F,3-45-6,Minamiotsuka, Toshima-Ku,  
Tokyo, 170-0005,Japan  
Tel: +81-3-6262-8932  
Fax: +81-3-6262-8933  
Email: info.jp@rigol.com

**KOREA**  
RIGOL KOREA CO., LTD.  
5F, 222, Gonghang-daero,  
Gangseo-gu, Seoul, Republic of Korea  
Tel: +82-2-6953-4466  
Fax: +82-2-6953-4422  
Email: info.kr@rigol.com

**For Assistance in Other Countries**  
Email: info.int@rigol.com

---

RIGOL® is the trademark of RIGOL TECHNOLOGIES CO., LTD. Product information in this document is subject to update without notice. For the latest information about RIGOL's products, applications and services, please contact local RIGOL channel partners or access RIGOL official website: www.rigol.com
