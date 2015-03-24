Raspi -> MPU6050

Pin 1 -> VCC
Pin 9 -> GND
Pin 5 -> SCL
Pin 3 -> SDA



dwc_otg.lpm_enable=0 console=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait