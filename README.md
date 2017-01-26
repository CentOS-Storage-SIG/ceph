CentOS Storage SIG: Ceph Jewel
==============================
The [CentOS Storage SIG for Ceph](https://wiki.centos.org/SpecialInterestGroup/Storage/)
used to maintain a dist-git like repository here in order to package and mirror
Ceph for the CentOS community.

We have since then decided to re-build Ceph from the source RPMs provided
[straight from upstream](http://download.ceph.com/rpm-jewel/el7/SRPMS/).

The spec file is kept here and versioned for reference purposes.

The contents of this repository are still available in the Git source code
management system.  To see the contents of this repository before we moved
away from dist-git, please check out the previous commits.

Build and tag information
-------------------------
Builds for Ceph for CentOS by the storage SIG are done through the
[Community Build System](https://wiki.centos.org/HowTos/CommunityBuildSystem) (CBS).

You can find the [tags](https://cbs.centos.org/koji/search?match=glob&type=tag&terms=storage7-ceph-jewel*)
and the [builds](https://cbs.centos.org/koji/packageinfo?packageID=534)
directly in the CBS interface.

Package and mirror availability
-------------------------------
Installing the package **centos-release-ceph-jewel** from CentOS extras will
provide the stable and testing repositories for the Jewel release of Ceph.

The testing repository is disabled by default but you can enable it to test an
upcoming release.
