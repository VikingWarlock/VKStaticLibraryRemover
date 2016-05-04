###VKRemove
####A Small Tool to remove some third party library from your static library

---
####Example:
#####I have a static library contains some third-party libraries:
	Masonary
	JFMinimalNotification
	FCFileManager
	.....
#####Now I need to regenerate a new static library that remove those lib from my static library. Here's the normal steps:
	1. lipo * -thin [platform] dir/new.a
	2. ar -t dir/new.a
	3. cd dir && ar xv new.a
	4. rm *MAS*
	...rm
	5.cd ..
	6. ar rcs lib_1.a dir/*.o 
	
#####after these step , I can only got a clean static library for `ONE` Platform.Which means I have to do maybe 3 times more...
#####and after that I have to combine them
	lipo -create ... -output new_clean_static_lib.a

---
###Now I make a small tool to fix this
####Function 1
	python VKRemove.py -lp xxx.a
####Returns
	This library contains:i386 armv7 x86_64 arm64
	
####Function 2
	python VKRemove.py -lb xxx.a
####Return the packages in your static library
	...'View+MASAdditions.o', 'ViewController+MASAdditions.o', 'XuanWheelBluetoothManager.o'...
	
#Function 3
	python VKRemove.py -i XuanWheelSDK.a -rm FCFileManager HMSegmentedControl- JFMinimalNotification   UIView+Round UIImage+ImageEffects.o MAS
#Return
`I can get a static library for multi-platform and without those libraries`
####And the new library will be named xxx.a.new

####Wait A Moment
####What is the "-" used for in the function 3?

python VKRemove.py -i XuanWheelSDK.a -rm FCFileManager `HMSegmentedControl-` JFMinimalNotification   UIView+Round UIImage+ImageEffects.o MAS

####Well when I delete the .o files I use the command rm \*PackageName\* rather than PackageName\*
####So if you have a class name really really seem like a static library.

####For example :HMSegmentedControl and VKHMSegmentedControl,perhaps you can use the "-"

##This is used for iOS
##If you like it please star it
[Twitter Me](https://twitter.com/VKWK_Viking)