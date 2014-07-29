##usfs: USFS Shared FileSystem
==============================


##This is a work in progress and is not ready for general use.

-----

`usfs` is a peer-to-peer filesystem that does not require centralized resources.


#####How to Use: 

1. Download and install FUSE for your operating system.
	
2. Download usfs.

3. Start the usfs server via: 

4. Start a usfs client using Python 2.7.8.  


#####Extending: 

`USFSIOBase` is an abstract base class containing the common methods for interacting with a simple filesystem.

-----

#####Troubleshooting:

If you receive an error the looks like:


    EnvironmentError: Unable to find libfuse


you likely need to install libfuse.  Note that as of this update to the README (Jul 2014), installing fuse via "Homebrew" does not work.

OSX: Get FUSE from: http://osxfuse.github.io/ and follow the instructions on installation.

Linux, Debian-based: `aptitude install fuse`

Other platforms: Find and install fuse.


