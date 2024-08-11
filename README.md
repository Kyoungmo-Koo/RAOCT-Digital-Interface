# RAOCT_Digital_Interface

Software Setup:

1. First, please bring in the txt file that has one position per line. And that line should contain 8 hexadecimal numbers. (First 4 hexadecimal numbers : X position, Last 4 hexadecimal numbers : Y position)
   
2. Count the number of lines in txt, and put numbers in STM32.c code, following the comments.
   
   For instance, RasterScan pattern which with Resolution of 512 * 512 and amplitude of 3 will has 100224 positions.
   Let's say we are dividing those positions into 32 chunks. So one chunk will have 3132 positions. For STM32, it is capable of containing two chunks inside the buffer, so that it can use TxCpltCallback and TxHalfCpltCallback functions. So number of positions would be 2 * 3132 = 6264
   (Check EnginePattern_amp3_res512_hexadecimal_downsample.txt file)
   NUM_OF_POSITIONS = 6264
   NUM_OF_POSITIONS_PER_CHUNK = 6264 / 2 = 3132;
   NUM_OF_BYTES_PER_CHUNK = 6264 * 2 = 12528;
   Configure the size of txData and rxData as 6264.

4. Now, STM32 software setup is complete. Let's setup Desktop.c code.
  Check if we have "ftd2xx.h", "libmpsse_spi.h", "Windows.h" files at correct place. Also, D2xx driver should be installed in computer. These are mandatory to use FTDI USB2SPI cable.

5. Check the COM port that is connected to ST-Link of STM32 and put that COM PORT into "COM6" place of the code.
Then, check if we have our txt file that we will use, is at the right place so that the code can read txt file.

6. Write the NUM_OF_POSITIONS_PER_CHUNK which is half of the variable NUM_OF_POSITIONS in STM32.c. Also, don't forget to match COUNT variable with that of STM32.c. Additionally, txt files that are uploaded to this repositories work well with CHUNK_NUM of 32, but if scan pattern is longer or shorter, adjust CHUNK_NUM variable considering the full scan pattern's length.

7. Now we will run the code. First, run STM32.c. When it is complete, run Desktop.c. Press "0" and ENTER key, then you will see "sent" on Debug console. Now, run oct.py code and press "start" on User Interface.
   
8. Finally, scan image will appear on the screen. When scan is complete, open data.csv file that contains information of position feedback from servo driver.

    
