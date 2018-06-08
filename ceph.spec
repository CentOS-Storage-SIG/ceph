# vim: set noexpandtab ts=8 sw=8 :
#
# spec file for package ceph
#
# Copyright (C) 2004-2017 The Ceph Project Developers. See COPYING file
# at the top-level directory of this distribution and at
# https://github.com/ceph/ceph/blob/master/COPYING
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon.
#
# This file is under the GNU Lesser General Public License, version 2.1
#
# Please submit bugfixes or comments via http://tracker.ceph.com/
#
%bcond_without ocf
%bcond_with make_check
%ifarch s390 s390x
%bcond_with tcmalloc
%else
%bcond_without tcmalloc
%endif
%if 0%{?fedora} || 0%{?rhel}
%bcond_without selinux
%bcond_without ceph_test_package
%bcond_without cephfs_java
%bcond_without lttng
%global _remote_tarball_prefix https://download.ceph.com/tarballs/
%endif
%if 0%{?suse_version}
%bcond_with selinux
%bcond_with ceph_test_package
%bcond_with cephfs_java
#Compat macro for new _fillupdir macro introduced in Nov 2017
%if ! %{defined _fillupdir}
%global _fillupdir /var/adm/fillup-templates
%endif
%if 0%{?is_opensuse}
%bcond_without lttng
%else
%ifarch x86_64 aarch64
%bcond_without lttng
%else
%bcond_with lttng
%endif
%endif
%endif
%if 0%{?suse_version} >= 1500
%bcond_with python2
%else
%bcond_without python2
%endif
%if 0%{without python2}
%global _defined_if_python2_absent 1
%endif

%if 0%{?rhel}
%global _python_buildid ''
%else
%global _python_buildid %{?_defined_if_python2_absent:%{python3_pkgversion}}
%endif

%if %{with selinux}
# get selinux policy version
%{!?_selinux_policy_version: %global _selinux_policy_version 0.0.0}
%endif

%{!?_udevrulesdir: %global _udevrulesdir /lib/udev/rules.d}
%{!?tmpfiles_create: %global tmpfiles_create systemd-tmpfiles --create}
%{!?python3_pkgversion: %global python3_pkgversion 3}
# define _python_buildid macro which will expand to the empty string when
# building with python2


# unify libexec for all targets
%global _libexecdir %{_exec_prefix}/lib

# disable dwz which compresses the debuginfo
%global _find_debuginfo_dwz_opts %{nil}

#################################################################################
# main package definition
#################################################################################
Name:		ceph
Version:	13.2.0
Release:	0%{?dist}
%if 0%{?fedora} || 0%{?rhel}
Epoch:		2
%endif

# define _epoch_prefix macro which will expand to the empty string if epoch is
# undefined
%global _epoch_prefix %{?epoch:%{epoch}:}

Summary:	User space components of the Ceph file system
License:	LGPL-2.1 and CC-BY-SA-3.0 and GPL-2.0 and BSL-1.0 and BSD-3-Clause and MIT
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
URL:		http://ceph.com/
Source0:	%{?_remote_tarball_prefix}ceph-13.2.0.tar.bz2
%if 0%{?suse_version}
# _insert_obs_source_lines_here
%if 0%{?is_opensuse}
ExclusiveArch:  x86_64 aarch64 ppc64 ppc64le
%else
ExclusiveArch:  x86_64 aarch64 ppc64le s390x
%endif
%endif
#################################################################################
# dependencies that apply across all distro families
#################################################################################
Requires:       ceph-osd = %{_epoch_prefix}%{version}-%{release}
Requires:       ceph-mds = %{_epoch_prefix}%{version}-%{release}
Requires:       ceph-mgr = %{_epoch_prefix}%{version}-%{release}
Requires:       ceph-mon = %{_epoch_prefix}%{version}-%{release}
Requires(post):	binutils
%if 0%{with cephfs_java}
BuildRequires:	java-devel
BuildRequires:	sharutils
%endif
%if 0%{with selinux}
BuildRequires:	checkpolicy
BuildRequires:	selinux-policy-devel
%endif
BuildRequires:	bc
BuildRequires:	gperf
BuildRequires:  cmake
BuildRequires:	cryptsetup
BuildRequires:	fuse-devel
%if 0%{?rhel} == 7
# devtoolset offers newer make and valgrind-devel, but the old ones are good
# enough.
BuildRequires:	devtoolset-7-gcc-c++
%else
BuildRequires:	gcc-c++
%endif
BuildRequires:	gdbm
%if 0%{with tcmalloc}
BuildRequires:	gperftools-devel >= 2.4
%endif
BuildRequires:  jq
BuildRequires:	leveldb-devel > 1.2
BuildRequires:	libaio-devel
BuildRequires:	libblkid-devel >= 2.17
BuildRequires:	libcurl-devel
BuildRequires:	libudev-devel
BuildRequires:	liboath-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libuuid-devel
BuildRequires:	make
BuildRequires:	parted
BuildRequires:	perl
BuildRequires:	pkgconfig
BuildRequires:  procps
BuildRequires:	python%{_python_buildid}
BuildRequires:	python%{_python_buildid}-devel
BuildRequires:	python%{_python_buildid}-nose
BuildRequires:	python%{_python_buildid}-requests
BuildRequires:	python%{_python_buildid}-virtualenv
BuildRequires:	snappy-devel
%if 0%{with make_check}
BuildRequires:	socat
%endif
BuildRequires:	udev
BuildRequires:	util-linux
BuildRequires:	valgrind-devel
BuildRequires:	which
BuildRequires:	xfsprogs
BuildRequires:	xfsprogs-devel
BuildRequires:	xmlstarlet
BuildRequires:	yasm

#################################################################################
# distro-conditional dependencies
#################################################################################
%if 0%{?suse_version}
BuildRequires:  pkgconfig(systemd)
BuildRequires:	systemd-rpm-macros
BuildRequires:	systemd
%{?systemd_requires}
PreReq:		%fillup_prereq
BuildRequires:	net-tools
BuildRequires:	libbz2-devel
BuildRequires:  btrfsprogs
BuildRequires:	mozilla-nss-devel
BuildRequires:	keyutils-devel
BuildRequires:  libopenssl-devel
BuildRequires:  lsb-release
BuildRequires:  openldap2-devel
BuildRequires:  cunit-devel
BuildRequires:	python%{_python_buildid}-base
BuildRequires:	python%{_python_buildid}-Cython
BuildRequires:	python%{_python_buildid}-PrettyTable
BuildRequires:	python%{_python_buildid}-Sphinx
BuildRequires:  rdma-core-devel
BuildRequires:	liblz4-devel >= 1.7
%endif
%if 0%{?fedora} || 0%{?rhel}
Requires:	systemd
BuildRequires:  boost-random
BuildRequires:	btrfs-progs
BuildRequires:	nss-devel
BuildRequires:	keyutils-libs-devel
BuildRequires:	libibverbs-devel
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel
BuildRequires:  CUnit-devel
BuildRequires:  redhat-lsb-core
BuildRequires:	Cython%{_python_buildid}
BuildRequires:	python%{_python_buildid}-prettytable
BuildRequires:	python%{_python_buildid}-sphinx
BuildRequires:	lz4-devel >= 1.7
%endif
# python34-... for RHEL, python3-... for all other supported distros
%if 0%{?rhel}
BuildRequires:	python34-devel
BuildRequires:	python34-setuptools
BuildRequires:	python34-Cython
%else
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-Cython
%endif
# distro-conditional make check dependencies
%if 0%{with make_check}
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	python%{_python_buildid}-cherrypy
BuildRequires:	python%{_python_buildid}-routes
BuildRequires:	python%{_python_buildid}-pecan
BuildRequires:	python%{_python_buildid}-werkzeug
BuildRequires:	python%{_python_buildid}-tox
BuildRequires:	python%{_python_buildid}-coverage
%if 0%{?fedora}
BuildRequires:	python%{_python_buildid}-bcrypt
%endif
%if 0%{?rhel}
BuildRequires:	py-bcrypt
%endif
%endif
%if 0%{?suse_version}
BuildRequires:	python%{_python_buildid}-CherryPy
BuildRequires:	python%{_python_buildid}-Routes
BuildRequires:	python%{_python_buildid}-Werkzeug
BuildRequires:	python%{_python_buildid}-pecan
BuildRequires:	python%{_python_buildid}-numpy-devel
BuildRequires:	python%{_python_buildid}-bcrypt
BuildRequires:	python%{_python_buildid}-tox
BuildRequires:	python%{_python_buildid}-coverage
%endif
%endif
# lttng and babeltrace for rbd-replay-prep
%if %{with lttng}
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	lttng-ust-devel
BuildRequires:	libbabeltrace-devel
%endif
%if 0%{?suse_version}
BuildRequires:	lttng-ust-devel
BuildRequires:  babeltrace-devel
%endif
%endif
%if 0%{?suse_version}
BuildRequires:	libexpat-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	expat-devel
%endif
#hardened-cc1
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:  redhat-rpm-config
%endif

%description
Ceph is a massively scalable, open-source, distributed storage system that runs
on commodity hardware and delivers object, block and file system storage.


#################################################################################
# subpackages
#################################################################################
%package base
Summary:       Ceph Base Package
%if 0%{?suse_version}
Group:         System/Filesystems
%endif
Requires:      ceph-common = %{_epoch_prefix}%{version}-%{release}
Requires:      librbd1 = %{_epoch_prefix}%{version}-%{release}
Requires:      librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:      libcephfs2 = %{_epoch_prefix}%{version}-%{release}
Requires:      librgw2 = %{_epoch_prefix}%{version}-%{release}
%if 0%{with selinux}
Requires:      ceph-selinux = %{_epoch_prefix}%{version}-%{release}
%endif
Requires:      cryptsetup
Requires:      e2fsprogs
Requires:      findutils
Requires:      grep
Requires:      logrotate
Requires:      parted
Requires:      psmisc
Requires:      python%{_python_buildid}-requests
Requires:      python%{_python_buildid}-setuptools
Requires:      util-linux
Requires:      xfsprogs
Requires:      which
%if 0%{?fedora} || 0%{?rhel}
Requires:      gdisk
%endif
%if 0%{?suse_version}
Recommends:    chrony
Requires:      gptfdisk
%endif
%description base
Base is the package that includes all the files shared amongst ceph servers

%package -n ceph-common
Summary:	Ceph Common
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:	libcephfs2 = %{_epoch_prefix}%{version}-%{release}
Requires:	python%{_python_buildid}-rados = %{_epoch_prefix}%{version}-%{release}
Requires:	python%{_python_buildid}-rbd = %{_epoch_prefix}%{version}-%{release}
Requires:	python%{_python_buildid}-cephfs = %{_epoch_prefix}%{version}-%{release}
Requires:	python%{_python_buildid}-rgw = %{_epoch_prefix}%{version}-%{release}
%if 0%{?fedora} || 0%{?rhel}
Requires:	python%{_python_buildid}-prettytable
Requires:	python%{_python_buildid}-requests
%endif
%if 0%{?suse_version}
Requires:	python%{_python_buildid}-PrettyTable
Requires:	python%{_python_buildid}-requests
%endif
%{?systemd_requires}
%if 0%{?suse_version}
Requires(pre):	pwdutils
%endif
%description -n ceph-common
Common utilities to mount and interact with a ceph storage cluster.
Comprised of files that are common to Ceph clients and servers.

%package mds
Summary:	Ceph Metadata Server Daemon
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}-%{release}
%description mds
ceph-mds is the metadata server daemon for the Ceph distributed file system.
One or more instances of ceph-mds collectively manage the file system
namespace, coordinating access to the shared OSD cluster.

%package mon
Summary:	Ceph Monitor Daemon
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}-%{release}
%description mon
ceph-mon is the cluster monitor daemon for the Ceph distributed file
system. One or more instances of ceph-mon form a Paxos part-time
parliament cluster that provides extremely reliable and durable storage
of cluster membership, configuration, and state.

%package mgr
Summary:        Ceph Manager Daemon
%if 0%{?suse_version}
Group:          System/Filesystems
%endif
Requires:       ceph-base = %{_epoch_prefix}%{version}-%{release}
%if 0%{?fedora} || 0%{?rhel}
Requires:       python%{_python_buildid}-cherrypy
Requires:       python%{_python_buildid}-routes
Requires:       python%{_python_buildid}-jinja2
Requires:       python%{_python_buildid}-pecan
Requires:       python%{_python_buildid}-werkzeug
Requires:       pyOpenSSL%{_python_buildid}
%if 0%{?fedora}
Requires:	python%{_python_buildid}-bcrypt
%endif
%if 0%{?rhel}
Requires:	py-bcrypt
%endif
%endif
%if 0%{?suse_version}
Requires:       python%{_python_buildid}-CherryPy
Requires:       python%{_python_buildid}-Routes
Requires:       python%{_python_buildid}-Jinja2
Requires:       python%{_python_buildid}-Werkzeug
Requires:       python%{_python_buildid}-pecan
Requires:       python%{_python_buildid}-pyOpenSSL
Requires:       python%{_python_buildid}-bcrypt
Recommends:     python%{_python_buildid}-influxdb
%endif
%description mgr
ceph-mgr enables python modules that provide services (such as the REST
module derived from Calamari) and expose CLI hooks.  ceph-mgr gathers
the cluster maps, the daemon metadata, and performance counters, and
exposes all these to the python modules.

%package fuse
Summary:	Ceph fuse-based client
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:       fuse
%description fuse
FUSE based client for Ceph distributed network file system

%package -n rbd-fuse
Summary:	Ceph fuse-based client
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
%description -n rbd-fuse
FUSE based client to map Ceph rbd images to files

%package -n rbd-mirror
Summary:	Ceph daemon for mirroring RBD images
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-common = %{_epoch_prefix}%{version}-%{release}
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
%description -n rbd-mirror
Daemon for mirroring RBD images between Ceph clusters, streaming
changes asynchronously.

%package -n rbd-nbd
Summary:	Ceph RBD client base on NBD
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
%description -n rbd-nbd
NBD based client to map Ceph rbd images to local device

%package radosgw
Summary:	Rados REST gateway
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-common = %{_epoch_prefix}%{version}-%{release}
%if 0%{with selinux}
Requires:	ceph-selinux = %{_epoch_prefix}%{version}-%{release}
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:	librgw2 = %{_epoch_prefix}%{version}-%{release}
%if 0%{?rhel} || 0%{?fedora}
Requires:	mailcap
%endif
%description radosgw
RADOS is a distributed object store used by the Ceph distributed
storage system.  This package provides a REST gateway to the
object store that aims to implement a superset of Amazon's S3
service as well as the OpenStack Object Storage ("Swift") API.

%if %{with ocf}
%package resource-agents
Summary:	OCF-compliant resource agents for Ceph daemons
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}
Requires:	resource-agents
%description resource-agents
Resource agents for monitoring and managing Ceph daemons
under Open Cluster Framework (OCF) compliant resource
managers such as Pacemaker.
%endif

%package osd
Summary:	Ceph Object Storage Daemon
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}-%{release}
Requires:	lvm2
%description osd
ceph-osd is the object storage daemon for the Ceph distributed file
system.  It is responsible for storing objects on a local file system
and providing access to them over the network.

%package -n librados2
Summary:	RADOS distributed object store client library
%if 0%{?suse_version}
Group:		System/Libraries
%endif
%if 0%{?rhel} || 0%{?fedora}
Obsoletes:	ceph-libs < %{_epoch_prefix}%{version}-%{release}
%endif
%description -n librados2
RADOS is a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to access the distributed object
store using a simple file-like interface.

%package -n librados-devel
Summary:	RADOS headers
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	librados2-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	librados2-devel < %{_epoch_prefix}%{version}-%{release}
%description -n librados-devel
This package contains libraries and headers needed to develop programs
that use RADOS object store.

%package -n librgw2
Summary:	RADOS gateway client library
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
%description -n librgw2
This package provides a library implementation of the RADOS gateway
(distributed object store with S3 and Swift personalities).

%package -n librgw-devel
Summary:	RADOS gateway client library
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	librados-devel = %{_epoch_prefix}%{version}-%{release}
Requires:	librgw2 = %{_epoch_prefix}%{version}-%{release}
Provides:	librgw2-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	librgw2-devel < %{_epoch_prefix}%{version}-%{release}
%description -n librgw-devel
This package contains libraries and headers needed to develop programs
that use RADOS gateway client library.

%if 0%{with python2}
%package -n python-rgw
Summary:	Python 2 libraries for the RADOS gateway
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
Requires:	librgw2 = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rados = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	python-ceph < %{_epoch_prefix}%{version}-%{release}
%description -n python-rgw
This package contains Python 2 libraries for interacting with Cephs RADOS
gateway.
%else

%package -n python%{python3_pkgversion}-rgw
Summary:	Python 3 libraries for the RADOS gateway
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
Requires:	librgw2 = %{_epoch_prefix}%{version}-%{release}
Requires:	python%{python3_pkgversion}-rados = %{_epoch_prefix}%{version}-%{release}
%description -n python%{python3_pkgversion}-rgw
This package contains Python 3 libraries for interacting with Cephs RADOS
gateway.
%endif
%endif

%if 0%{with python2}
%package -n python-rados
Summary:	Python 2 libraries for the RADOS object store
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	python-ceph < %{_epoch_prefix}%{version}-%{release}
%description -n python-rados
This package contains Python 2 libraries for interacting with Cephs RADOS
object store.
%endif

%else
%package -n python%{python3_pkgversion}-rados
Summary:	Python 3 libraries for the RADOS object store
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
Requires:	python%{python3_pkgversion}
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
%description -n python%{python3_pkgversion}-rados
This package contains Python 3 libraries for interacting with Cephs RADOS
object store.
%endif
%endif

%package -n libradosstriper1
Summary:	RADOS striping interface
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
%description -n libradosstriper1
Striping interface built on top of the rados library, allowing
to stripe bigger objects onto several standard rados objects using
an interface very similar to the rados one.

%package -n libradosstriper-devel
Summary:	RADOS striping interface headers
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	libradosstriper1 = %{_epoch_prefix}%{version}-%{release}
Requires:	librados-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	libradosstriper1-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	libradosstriper1-devel < %{_epoch_prefix}%{version}-%{release}
%description -n libradosstriper-devel
This package contains libraries and headers needed to develop programs
that use RADOS striping interface.

%package -n librbd1
Summary:	RADOS block device client library
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
%if 0%{?suse_version}
Requires(post): coreutils
%endif
%if 0%{?rhel} || 0%{?fedora}
Obsoletes:	ceph-libs < %{_epoch_prefix}%{version}-%{release}
%endif
%description -n librbd1
RBD is a block device striped across multiple distributed objects in
RADOS, a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to manage these block devices.

%package -n librbd-devel
Summary:	RADOS block device headers
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
Requires:	librados-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	librbd1-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	librbd1-devel < %{_epoch_prefix}%{version}-%{release}
%description -n librbd-devel
This package contains libraries and headers needed to develop programs
that use RADOS block device.

%if 0%{with python2}
%package -n python-rbd
Summary:	Python 2 libraries for the RADOS block device
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rados = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	python-ceph < %{_epoch_prefix}%{version}-%{release}
%description -n python-rbd
This package contains Python 2 libraries for interacting with Cephs RADOS
block device.
%endif

%else
%package -n python%{python3_pkgversion}-rbd
Summary:	Python 3 libraries for the RADOS block device
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
Requires:	python%{python3_pkgversion}-rados = %{_epoch_prefix}%{version}-%{release}
%description -n python%{python3_pkgversion}-rbd
This package contains Python 3 libraries for interacting with Cephs RADOS
block device.
%endif
%endif

%package -n libcephfs2
Summary:	Ceph distributed file system client library
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Obsoletes:	libcephfs1
%if 0%{?rhel} || 0%{?fedora}
Obsoletes:	ceph-libs < %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-libcephfs
%endif
%description -n libcephfs2
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability. This is a shared library
allowing applications to access a Ceph distributed file system via a
POSIX-like interface.

%package -n libcephfs-devel
Summary:	Ceph distributed file system headers
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	libcephfs2 = %{_epoch_prefix}%{version}-%{release}
Requires:	librados-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	libcephfs2-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	libcephfs2-devel < %{_epoch_prefix}%{version}-%{release}
%description -n libcephfs-devel
This package contains libraries and headers needed to develop programs
that use Cephs distributed file system.

%if 0%{with python2}
%package -n python-cephfs
Summary:	Python 2 libraries for Ceph distributed file system
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
Requires:	libcephfs2 = %{_epoch_prefix}%{version}-%{release}
%if 0%{?suse_version}
Recommends: python-rados = %{_epoch_prefix}%{version}-%{release}
%endif
Obsoletes:	python-ceph < %{_epoch_prefix}%{version}-%{release}
%description -n python-cephfs
This package contains Python 2 libraries for interacting with Cephs distributed
file system.
%endif

%else
%package -n python%{python3_pkgversion}-cephfs
Summary:	Python 3 libraries for Ceph distributed file system
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
Requires:	libcephfs2 = %{_epoch_prefix}%{version}-%{release}
Requires:	python%{python3_pkgversion}-rados = %{_epoch_prefix}%{version}-%{release}
%description -n python%{python3_pkgversion}-cephfs
This package contains Python 3 libraries for interacting with Cephs distributed
file system.
%endif
%endif

%if 0%{with python2}
%package -n python%{python3_pkgversion}-ceph-argparse
Summary:	Python 3 utility libraries for Ceph CLI
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
%description -n python%{python3_pkgversion}-ceph-argparse
This package contains types and routines for Python 3 used by the Ceph CLI as
well as the RESTful interface. These have to do with querying the daemons for
command-description information, validating user command input against those
descriptions, and submitting the command to the appropriate daemon.
%endif

%if 0%{with ceph_test_package}
%package -n ceph-test
Summary:	Ceph benchmarks and test tools
%if 0%{?suse_version}
Group:		System/Benchmark
%endif
Requires:	ceph-common = %{_epoch_prefix}%{version}-%{release}
Requires:	xmlstarlet
Requires:	jq
Requires:	socat
%description -n ceph-test
This package contains Ceph benchmarks and test tools.
%endif

%if 0%{with cephfs_java}

%package -n libcephfs_jni1
Summary:	Java Native Interface library for CephFS Java bindings
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	java
Requires:	libcephfs2 = %{_epoch_prefix}%{version}-%{release}
%description -n libcephfs_jni1
This package contains the Java Native Interface library for CephFS Java
bindings.

%package -n libcephfs_jni-devel
Summary:	Development files for CephFS Java Native Interface library
%if 0%{?suse_version}
Group:		Development/Libraries/Java
%endif
Requires:	java
Requires:	libcephfs_jni1 = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	libcephfs_jni1-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	libcephfs_jni1-devel < %{_epoch_prefix}%{version}-%{release}
%description -n libcephfs_jni-devel
This package contains the development files for CephFS Java Native Interface
library.

%package -n cephfs-java
Summary:	Java libraries for the Ceph File System
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	java
Requires:	libcephfs_jni1 = %{_epoch_prefix}%{version}-%{release}
Requires:       junit
BuildRequires:  junit
%description -n cephfs-java
This package contains the Java libraries for the Ceph File System.

%endif

%package -n rados-objclass-devel
Summary:        RADOS object class development kit
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:       librados2-devel = %{_epoch_prefix}%{version}-%{release}
%description -n rados-objclass-devel
This package contains libraries and headers needed to develop RADOS object
class plugins.

%if 0%{with selinux}

%package selinux
Summary:	SELinux support for Ceph MON, OSD and MDS
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}-%{release}
Requires:	policycoreutils, libselinux-utils
Requires(post):	ceph-base = %{_epoch_prefix}%{version}-%{release}
Requires(post): selinux-policy-base >= %{_selinux_policy_version}, policycoreutils, gawk
Requires(postun): policycoreutils
%description selinux
This package contains SELinux support for Ceph MON, OSD and MDS. The package
also performs file-system relabelling which can take a long time on heavily
populated file-systems.

%endif

%if 0%{with python2}
%package -n python-ceph-compat
Summary:	Compatibility package for Cephs python libraries
%if 0%{?suse_version}
Group:		Development/Libraries/Python
%endif
Obsoletes:	python-ceph
Requires:	python-rados = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rbd = %{_epoch_prefix}%{version}-%{release}
Requires:	python-cephfs = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rgw = %{_epoch_prefix}%{version}-%{release}
Provides:	python-ceph
%description -n python-ceph-compat
This is a compatibility package to accommodate python-ceph split into
python-rados, python-rbd, python-rgw and python-cephfs. Packages still
depending on python-ceph should be fixed to depend on python-rados,
python-rbd, python-rgw or python-cephfs instead.
%endif

#################################################################################
# common
#################################################################################
%prep
%autosetup -p1 -n ceph-13.2.0

%build

%if 0%{?rhel} == 7
. /opt/rh/devtoolset-7/enable
%endif

%if 0%{with cephfs_java}
# Find jni.h
for i in /usr/{lib64,lib}/jvm/java/include{,/linux}; do
    [ -d $i ] && java_inc="$java_inc -I$i"
done
%endif

%if 0%{?suse_version}
# the following setting fixed an OOM condition we once encountered in the OBS
RPM_OPT_FLAGS="$RPM_OPT_FLAGS --param ggc-min-expand=20 --param ggc-min-heapsize=32768"
%endif

export CPPFLAGS="$java_inc"
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

# Parallel build settings ...
CEPH_MFLAGS_JOBS="%{?_smp_mflags}"
CEPH_SMP_NCPUS=$(echo "$CEPH_MFLAGS_JOBS" | sed 's/-j//')
%if 0%{?__isa_bits} == 32
# 32-bit builds can use 3G memory max, which is not enough even for -j2
CEPH_SMP_NCPUS="1"
%endif
# do not eat all memory
echo "Available memory:"
free -h
echo "System limits:"
ulimit -a
if test -n "$CEPH_SMP_NCPUS" -a "$CEPH_SMP_NCPUS" -gt 1 ; then
    mem_per_process=1800
    max_mem=$(LANG=C free -m | sed -n "s|^Mem: *\([0-9]*\).*$|\1|p")
    max_jobs="$(($max_mem / $mem_per_process))"
    test "$CEPH_SMP_NCPUS" -gt "$max_jobs" && CEPH_SMP_NCPUS="$max_jobs" && echo "Warning: Reducing build parallelism to -j$max_jobs because of memory limits"
    test "$CEPH_SMP_NCPUS" -le 0 && CEPH_SMP_NCPUS="1" && echo "Warning: Not using parallel build at all because of memory limits"
fi
export CEPH_SMP_NCPUS
export CEPH_MFLAGS_JOBS="-j$CEPH_SMP_NCPUS"

env | sort

mkdir build
cd build
cmake .. \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_LIBEXECDIR=%{_libexecdir} \
    -DCMAKE_INSTALL_LOCALSTATEDIR=%{_localstatedir} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DCMAKE_INSTALL_MANDIR=%{_mandir} \
    -DCMAKE_INSTALL_DOCDIR=%{_docdir}/ceph \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DWITH_EMBEDDED=OFF \
    -DWITH_MANPAGE=ON \
    -DWITH_PYTHON3=OFF \
    -DWITH_MGR_DASHBOARD_FRONTEND=OFF \
%if %{with python2}
    -DWITH_PYTHON2=ON \
%else
    -DWITH_PYTHON2=OFF \
    -DMGR_PYTHON_VERSION=3 \
%endif
%if 0%{?rhel} && ! 0%{?centos}
    -DWITH_SUBMAN=ON \
%endif
%if 0%{without ceph_test_package}
    -DWITH_TESTS=OFF \
%endif
%if 0%{with cephfs_java}
    -DWITH_CEPHFS_JAVA=ON \
%endif
%if 0%{with selinux}
    -DWITH_SELINUX=ON \
%endif
%if %{with lttng}
    -DWITH_LTTNG=ON \
    -DWITH_BABELTRACE=ON \
%else
    -DWITH_LTTNG=OFF \
    -DWITH_BABELTRACE=OFF \
%endif
    $CEPH_EXTRA_CMAKE_ARGS \
%if 0%{with ocf}
    -DWITH_OCF=ON \
%endif
%ifarch aarch64 armv7hl mips mipsel ppc ppc64 ppc64le %{ix86} x86_64
    -DWITH_BOOST_CONTEXT=ON \
%else
    -DWITH_BOOST_CONTEXT=OFF \
%endif
    -DBOOST_J=$CEPH_SMP_NCPUS

make "$CEPH_MFLAGS_JOBS"


%if 0%{with make_check}
%check
# run in-tree unittests
cd build
ctest "$CEPH_MFLAGS_JOBS"
%endif


%install
pushd build
make DESTDIR=%{buildroot} install
# we have dropped sysvinit bits
rm -f %{buildroot}/%{_sysconfdir}/init.d/ceph
popd
install -m 0644 -D src/etc-rbdmap %{buildroot}%{_sysconfdir}/ceph/rbdmap
%if 0%{?fedora} || 0%{?rhel}
install -m 0644 -D etc/sysconfig/ceph %{buildroot}%{_sysconfdir}/sysconfig/ceph
%endif
%if 0%{?suse_version}
install -m 0644 -D etc/sysconfig/ceph %{buildroot}%{_fillupdir}/sysconfig.%{name}
%endif
install -m 0644 -D systemd/ceph.tmpfiles.d %{buildroot}%{_tmpfilesdir}/ceph-common.conf
install -m 0644 -D systemd/50-ceph.preset %{buildroot}%{_libexecdir}/systemd/system-preset/50-ceph.preset
mkdir -p %{buildroot}%{_sbindir}
install -m 0644 -D src/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/ceph
chmod 0644 %{buildroot}%{_docdir}/ceph/sample.ceph.conf
install -m 0644 -D COPYING %{buildroot}%{_docdir}/ceph/COPYING
install -m 0644 -D etc/sysctl/90-ceph-osd.conf %{buildroot}%{_sysctldir}/90-ceph-osd.conf

# firewall templates and /sbin/mount.ceph symlink
%if 0%{?suse_version}
install -m 0644 -D etc/sysconfig/SuSEfirewall2.d/services/ceph-mon %{buildroot}%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/ceph-mon
install -m 0644 -D etc/sysconfig/SuSEfirewall2.d/services/ceph-osd-mds %{buildroot}%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/ceph-osd-mds
mkdir -p %{buildroot}/sbin
ln -sf %{_sbindir}/mount.ceph %{buildroot}/sbin/mount.ceph
%endif

# udev rules
install -m 0644 -D udev/50-rbd.rules %{buildroot}%{_udevrulesdir}/50-rbd.rules
install -m 0644 -D udev/60-ceph-by-parttypeuuid.rules %{buildroot}%{_udevrulesdir}/60-ceph-by-parttypeuuid.rules
install -m 0644 -D udev/95-ceph-osd.rules %{buildroot}%{_udevrulesdir}/95-ceph-osd.rules

#set up placeholder directories
mkdir -p %{buildroot}%{_sysconfdir}/ceph
mkdir -p %{buildroot}%{_localstatedir}/run/ceph
mkdir -p %{buildroot}%{_localstatedir}/log/ceph
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/tmp
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mon
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/osd
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mds
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mgr
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/radosgw
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-osd
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-mds
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-rgw
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-mgr
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-rbd

%if 0%{?suse_version}
# create __pycache__ directories and their contents
%py3_compile %{buildroot}%{python3_sitelib}
%endif

%clean
rm -rf %{buildroot}

#################################################################################
# files and systemd scriptlets
#################################################################################
%files

%files base
%{_bindir}/crushtool
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/ceph-kvstore-tool
%{_bindir}/ceph-run
%{_bindir}/ceph-detect-init
%{_libexecdir}/systemd/system-preset/50-ceph.preset
%{_sbindir}/ceph-create-keys
%{_sbindir}/ceph-disk
%dir %{_libexecdir}/ceph
%{_libexecdir}/ceph/ceph_common.sh
%dir %{_libdir}/rados-classes
%{_libdir}/rados-classes/*
%dir %{_libdir}/ceph
%dir %{_libdir}/ceph/erasure-code
%{_libdir}/ceph/erasure-code/libec_*.so*
%dir %{_libdir}/ceph/compressor
%{_libdir}/ceph/compressor/libceph_*.so*
%ifarch x86_64
%dir %{_libdir}/ceph/crypto
%{_libdir}/ceph/crypto/libceph_*.so*
%endif
%if %{with lttng}
%{_libdir}/libos_tp.so*
%{_libdir}/libosd_tp.so*
%endif
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%if 0%{?fedora} || 0%{?rhel}
%config(noreplace) %{_sysconfdir}/sysconfig/ceph
%endif
%if 0%{?suse_version}
%{_fillupdir}/sysconfig.*
%config %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/ceph-mon
%config %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/ceph-osd-mds
%endif
%{_unitdir}/ceph-disk@.service
%{_unitdir}/ceph.target
%if 0%{with python2}
%{python_sitelib}/ceph_detect_init*
%{python_sitelib}/ceph_disk*
%else
%{python3_sitelib}/ceph_detect_init*
%{python3_sitelib}/ceph_disk*
%endif
%if 0%{with python2}
%dir %{python_sitelib}/ceph_volume
%{python_sitelib}/ceph_volume/*
%{python_sitelib}/ceph_volume-*
%else
%dir %{python3_sitelib}/ceph_volume
%{python3_sitelib}/ceph_volume/*
%{python3_sitelib}/ceph_volume-*
%endif
%{_mandir}/man8/ceph-deploy.8*
%{_mandir}/man8/ceph-detect-init.8*
%{_mandir}/man8/ceph-create-keys.8*
%{_mandir}/man8/ceph-disk.8*
%{_mandir}/man8/ceph-run.8*
%{_mandir}/man8/crushtool.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/ceph-kvstore-tool.8*
#set up placeholder directories
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/tmp
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-osd
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-mds
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-rgw
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-mgr
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-rbd

%post base
/sbin/ldconfig
%if 0%{?suse_version}
%fillup_only
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl preset ceph-disk@\*.service ceph.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-disk@\*.service ceph.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph.target >/dev/null 2>&1 || :
fi

%preun base
%if 0%{?suse_version}
%service_del_preun ceph-disk@\*.service ceph.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-disk@\*.service ceph.target
%endif

%postun base
/sbin/ldconfig
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-disk@\*.service ceph.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-disk@\*.service ceph.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-disk@\*.service > /dev/null 2>&1 || :
  fi
fi

%files common
%dir %{_docdir}/ceph
%doc %{_docdir}/ceph/sample.ceph.conf
%doc %{_docdir}/ceph/COPYING
%{_bindir}/ceph
%{_bindir}/ceph-authtool
%{_bindir}/ceph-conf
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-rbdnamer
%{_bindir}/ceph-syn
%{_bindir}/cephfs-data-scan
%{_bindir}/cephfs-journal-tool
%{_bindir}/cephfs-table-tool
%{_bindir}/rados
%{_bindir}/radosgw-admin
%{_bindir}/rbd
%{_bindir}/rbd-replay
%{_bindir}/rbd-replay-many
%{_bindir}/rbdmap
%{_sbindir}/mount.ceph
%if 0%{?suse_version}
/sbin/mount.ceph
%endif
%if %{with lttng}
%{_bindir}/rbd-replay-prep
%endif
%{_bindir}/ceph-post-file
%{_tmpfilesdir}/ceph-common.conf
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph-dencoder.8*
%{_mandir}/man8/ceph-rbdnamer.8*
%{_mandir}/man8/ceph-syn.8*
%{_mandir}/man8/ceph-post-file.8*
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/radosgw-admin.8*
%{_mandir}/man8/rbd.8*
%{_mandir}/man8/rbdmap.8*
%{_mandir}/man8/rbd-replay.8*
%{_mandir}/man8/rbd-replay-many.8*
%{_mandir}/man8/rbd-replay-prep.8*
%dir %{_datadir}/ceph/
%{_datadir}/ceph/known_hosts_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com.pub
%dir %{_sysconfdir}/ceph/
%config %{_sysconfdir}/bash_completion.d/ceph
%config %{_sysconfdir}/bash_completion.d/rados
%config %{_sysconfdir}/bash_completion.d/rbd
%config %{_sysconfdir}/bash_completion.d/radosgw-admin
%config(noreplace) %{_sysconfdir}/ceph/rbdmap
%{_unitdir}/rbdmap.service
%if 0%{with python2}
%{python_sitelib}/ceph_argparse.py*
%{python_sitelib}/ceph_daemon.py*
%else
%{python3_sitelib}/ceph_argparse.py
%{python3_sitelib}/__pycache__/ceph_argparse.cpython*.py*
%{python3_sitelib}/ceph_daemon.py
%{python3_sitelib}/__pycache__/ceph_daemon.cpython*.py*
%endif
%dir %{_udevrulesdir}
%{_udevrulesdir}/50-rbd.rules
%attr(3770,ceph,ceph) %dir %{_localstatedir}/log/ceph/
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/

%pre common
CEPH_GROUP_ID=167
CEPH_USER_ID=167
%if 0%{?rhel} || 0%{?fedora}
/usr/sbin/groupadd ceph -g $CEPH_GROUP_ID -o -r 2>/dev/null || :
/usr/sbin/useradd ceph -u $CEPH_USER_ID -o -r -g ceph -s /sbin/nologin -c "Ceph daemons" -d %{_localstatedir}/lib/ceph 2>/dev/null || :
%endif
%if 0%{?suse_version}
if ! getent group ceph >/dev/null ; then
    CEPH_GROUP_ID_OPTION=""
    getent group $CEPH_GROUP_ID >/dev/null || CEPH_GROUP_ID_OPTION="-g $CEPH_GROUP_ID"
    groupadd ceph $CEPH_GROUP_ID_OPTION -r 2>/dev/null || :
fi
if ! getent passwd ceph >/dev/null ; then
    CEPH_USER_ID_OPTION=""
    getent passwd $CEPH_USER_ID >/dev/null || CEPH_USER_ID_OPTION="-u $CEPH_USER_ID"
    useradd ceph $CEPH_USER_ID_OPTION -r -g ceph -s /sbin/nologin 2>/dev/null || :
fi
usermod -c "Ceph storage service" \
        -d %{_localstatedir}/lib/ceph \
        -g ceph \
        -s /sbin/nologin \
        ceph
%endif
exit 0

%post common
%tmpfiles_create %{_tmpfilesdir}/ceph-common.conf

%postun common
# Package removal cleanup
if [ "$1" -eq "0" ] ; then
    rm -rf %{_localstatedir}/log/ceph
    rm -rf %{_sysconfdir}/ceph
fi

%files mds
%{_bindir}/ceph-mds
%{_mandir}/man8/ceph-mds.8*
%{_unitdir}/ceph-mds@.service
%{_unitdir}/ceph-mds.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mds

%post mds
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-mds@\*.service ceph-mds.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-mds@\*.service ceph-mds.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-mds.target >/dev/null 2>&1 || :
fi

%preun mds
%if 0%{?suse_version}
%service_del_preun ceph-mds@\*.service ceph-mds.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-mds@\*.service ceph-mds.target
%endif

%postun mds
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-mds@\*.service ceph-mds.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-mds@\*.service ceph-mds.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mds@\*.service > /dev/null 2>&1 || :
  fi
fi

%files mgr
%{_bindir}/ceph-mgr
%{_libdir}/ceph/mgr
%{_unitdir}/ceph-mgr@.service
%{_unitdir}/ceph-mgr.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mgr

%post mgr
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-mgr@\*.service ceph-mgr.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-mgr@\*.service ceph-mgr.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-mgr.target >/dev/null 2>&1 || :
fi

%preun mgr
%if 0%{?suse_version}
%service_del_preun ceph-mgr@\*.service ceph-mgr.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-mgr@\*.service ceph-mgr.target
%endif

%postun mgr
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-mgr@\*.service ceph-mgr.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-mgr@\*.service ceph-mgr.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mgr@\*.service > /dev/null 2>&1 || :
  fi
fi

%files mon
%{_bindir}/ceph-mon
%{_bindir}/ceph-monstore-tool
%{_mandir}/man8/ceph-mon.8*
%{_unitdir}/ceph-mon@.service
%{_unitdir}/ceph-mon.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mon

%post mon
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-mon@\*.service ceph-mon.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-mon@\*.service ceph-mon.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-mon.target >/dev/null 2>&1 || :
fi

%preun mon
%if 0%{?suse_version}
%service_del_preun ceph-mon@\*.service ceph-mon.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-mon@\*.service ceph-mon.target
%endif

%postun mon
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-mon@\*.service ceph-mon.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-mon@\*.service ceph-mon.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mon@\*.service > /dev/null 2>&1 || :
  fi
fi

%files fuse
%{_bindir}/ceph-fuse
%{_mandir}/man8/ceph-fuse.8*
%{_sbindir}/mount.fuse.ceph
%{_unitdir}/ceph-fuse@.service
%{_unitdir}/ceph-fuse.target

%files -n rbd-fuse
%{_bindir}/rbd-fuse
%{_mandir}/man8/rbd-fuse.8*

%files -n rbd-mirror
%{_bindir}/rbd-mirror
%{_mandir}/man8/rbd-mirror.8*
%{_unitdir}/ceph-rbd-mirror@.service
%{_unitdir}/ceph-rbd-mirror.target

%post -n rbd-mirror
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-rbd-mirror@\*.service ceph-rbd-mirror.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-rbd-mirror.target >/dev/null 2>&1 || :
fi

%preun -n rbd-mirror
%if 0%{?suse_version}
%service_del_preun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif

%postun -n rbd-mirror
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-rbd-mirror@\*.service > /dev/null 2>&1 || :
  fi
fi

%files -n rbd-nbd
%{_bindir}/rbd-nbd
%{_mandir}/man8/rbd-nbd.8*

%files radosgw
%{_bindir}/radosgw
%{_bindir}/radosgw-token
%{_bindir}/radosgw-es
%{_bindir}/radosgw-object-expirer
%{_mandir}/man8/radosgw.8*
%dir %{_localstatedir}/lib/ceph/radosgw
%{_unitdir}/ceph-radosgw@.service
%{_unitdir}/ceph-radosgw.target

%post radosgw
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-radosgw@\*.service ceph-radosgw.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-radosgw@\*.service ceph-radosgw.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-radosgw.target >/dev/null 2>&1 || :
fi

%preun radosgw
%if 0%{?suse_version}
%service_del_preun ceph-radosgw@\*.service ceph-radosgw.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-radosgw@\*.service ceph-radosgw.target
%endif

%postun radosgw
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-radosgw@\*.service ceph-radosgw.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-radosgw@\*.service ceph-radosgw.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-radosgw@\*.service > /dev/null 2>&1 || :
  fi
fi

%files osd
%{_bindir}/ceph-clsinfo
%{_bindir}/ceph-bluestore-tool
%{_bindir}/ceph-objectstore-tool
%{_bindir}/ceph-osdomap-tool
%{_bindir}/ceph-osd
%{_libexecdir}/ceph/ceph-osd-prestart.sh
%{_sbindir}/ceph-volume
%{_sbindir}/ceph-volume-systemd
%dir %{_udevrulesdir}
%{_udevrulesdir}/60-ceph-by-parttypeuuid.rules
%{_udevrulesdir}/95-ceph-osd.rules
%{_mandir}/man8/ceph-clsinfo.8*
%{_mandir}/man8/ceph-osd.8*
%{_mandir}/man8/ceph-bluestore-tool.8*
%{_mandir}/man8/ceph-volume.8*
%{_mandir}/man8/ceph-volume-systemd.8*
%if 0%{?rhel} && ! 0%{?centos}
%attr(0755,-,-) %{_sysconfdir}/cron.hourly/subman
%endif
%{_unitdir}/ceph-osd@.service
%{_unitdir}/ceph-osd.target
%{_unitdir}/ceph-volume@.service
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/osd
%config(noreplace) %{_sysctldir}/90-ceph-osd.conf

%post osd
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-osd.target >/dev/null 2>&1 || :
fi
%if 0%{?sysctl_apply}
    %sysctl_apply 90-ceph-osd.conf
%else
    /usr/lib/systemd/systemd-sysctl %{_sysctldir}/90-ceph-osd.conf > /dev/null 2>&1 || :
%endif

%preun osd
%if 0%{?suse_version}
%service_del_preun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif

%postun osd
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-osd@\*.service ceph-volume@\*.service > /dev/null 2>&1 || :
  fi
fi

%if %{with ocf}

%files resource-agents
%dir %{_prefix}/lib/ocf
%dir %{_prefix}/lib/ocf/resource.d
%dir %{_prefix}/lib/ocf/resource.d/ceph
%attr(0755,-,-) %{_prefix}/lib/ocf/resource.d/ceph/rbd

%endif

%files -n librados2
%{_libdir}/librados.so.*
%dir %{_libdir}/ceph
%{_libdir}/ceph/libceph-common.so*
%if %{with lttng}
%{_libdir}/librados_tp.so.*
%endif

%post -n librados2 -p /sbin/ldconfig

%postun -n librados2 -p /sbin/ldconfig

%files -n librados-devel
%dir %{_includedir}/rados
%{_includedir}/rados/librados.h
%{_includedir}/rados/librados.hpp
%{_includedir}/rados/buffer.h
%{_includedir}/rados/buffer_fwd.h
%{_includedir}/rados/inline_memory.h
%{_includedir}/rados/page.h
%{_includedir}/rados/crc32c.h
%{_includedir}/rados/rados_types.h
%{_includedir}/rados/rados_types.hpp
%{_includedir}/rados/memory.h
%{_libdir}/librados.so
%if %{with lttng}
%{_libdir}/librados_tp.so
%endif
%{_bindir}/librados-config
%{_mandir}/man8/librados-config.8*

%if 0%{with python2}
%files -n python-rados
%{python_sitearch}/rados.so
%{python_sitearch}/rados-*.egg-info
%else

%files -n python%{python3_pkgversion}-rados
%{python3_sitearch}/rados.cpython*.so
%{python3_sitearch}/rados-*.egg-info
%endif

%files -n libradosstriper1
%{_libdir}/libradosstriper.so.*

%post -n libradosstriper1 -p /sbin/ldconfig

%postun -n libradosstriper1 -p /sbin/ldconfig

%files -n libradosstriper-devel
%dir %{_includedir}/radosstriper
%{_includedir}/radosstriper/libradosstriper.h
%{_includedir}/radosstriper/libradosstriper.hpp
%{_libdir}/libradosstriper.so

%files -n librbd1
%{_libdir}/librbd.so.*
%if %{with lttng}
%{_libdir}/librbd_tp.so.*
%endif

%post -n librbd1 -p /sbin/ldconfig

%postun -n librbd1 -p /sbin/ldconfig

%files -n librbd-devel
%dir %{_includedir}/rbd
%{_includedir}/rbd/librbd.h
%{_includedir}/rbd/librbd.hpp
%{_includedir}/rbd/features.h
%{_libdir}/librbd.so
%if %{with lttng}
%{_libdir}/librbd_tp.so
%endif

%files -n librgw2
%{_libdir}/librgw.so.*
%if %{with lttng}
%{_libdir}/librgw_op_tp.so*
%{_libdir}/librgw_rados_tp.so*
%endif

%post -n librgw2 -p /sbin/ldconfig

%postun -n librgw2 -p /sbin/ldconfig

%files -n librgw-devel
%dir %{_includedir}/rados
%{_includedir}/rados/librgw.h
%{_includedir}/rados/rgw_file.h
%{_libdir}/librgw.so

%if 0%{with python2}
%files -n python-rgw
%{python_sitearch}/rgw.so
%{python_sitearch}/rgw-*.egg-info
%else
%files -n python%{python3_pkgversion}-rgw
%{python3_sitearch}/rgw.cpython*.so
%{python3_sitearch}/rgw-*.egg-info
%endif

%if 0%{with python2}
%files -n python-rbd
%{python_sitearch}/rbd.so
%{python_sitearch}/rbd-*.egg-info
%else

%files -n python%{python3_pkgversion}-rbd
%{python3_sitearch}/rbd.cpython*.so
%{python3_sitearch}/rbd-*.egg-info
%endif

%files -n libcephfs2
%{_libdir}/libcephfs.so.*

%post -n libcephfs2 -p /sbin/ldconfig

%postun -n libcephfs2 -p /sbin/ldconfig

%files -n libcephfs-devel
%dir %{_includedir}/cephfs
%{_includedir}/cephfs/libcephfs.h
%{_includedir}/cephfs/ceph_statx.h
%{_libdir}/libcephfs.so

%if 0%{with python2}
%files -n python-cephfs
%{python_sitearch}/cephfs.so
%{python_sitearch}/cephfs-*.egg-info
%{python_sitelib}/ceph_volume_client.py*
%else

%files -n python%{python3_pkgversion}-cephfs
%{python3_sitearch}/cephfs.cpython*.so
%{python3_sitearch}/cephfs-*.egg-info
%{python3_sitelib}/ceph_volume_client.py
%{python3_sitelib}/__pycache__/ceph_volume_client.cpython*.py*
%endif

%if 0%{with python2}
%files -n python%{python3_pkgversion}-ceph-argparse
%{python3_sitelib}/ceph_argparse.py
%{python3_sitelib}/__pycache__/ceph_argparse.cpython*.py*
%{python3_sitelib}/ceph_daemon.py
%{python3_sitelib}/__pycache__/ceph_daemon.cpython*.py*
%endif

%if 0%{with ceph_test_package}
%files -n ceph-test
%{_bindir}/ceph-client-debug
%{_bindir}/ceph_bench_log
%{_bindir}/ceph_kvstorebench
%{_bindir}/ceph_multi_stress_watch
%{_bindir}/ceph_erasure_code
%{_bindir}/ceph_erasure_code_benchmark
%{_bindir}/ceph_omapbench
%{_bindir}/ceph_objectstore_bench
%{_bindir}/ceph_perf_objectstore
%{_bindir}/ceph_perf_local
%{_bindir}/ceph_perf_msgr_client
%{_bindir}/ceph_perf_msgr_server
%{_bindir}/ceph_psim
%{_bindir}/ceph_radosacl
%{_bindir}/ceph_rgw_jsonparser
%{_bindir}/ceph_rgw_multiparser
%{_bindir}/ceph_scratchtool
%{_bindir}/ceph_scratchtoolpp
%{_bindir}/ceph_test_*
%{_bindir}/ceph-coverage
%{_bindir}/ceph-debugpack
%{_mandir}/man8/ceph-debugpack.8*
%dir %{_libdir}/ceph
%{_libdir}/ceph/ceph-monstore-update-crush.sh
%endif

%if 0%{with cephfs_java}
%files -n libcephfs_jni1
%{_libdir}/libcephfs_jni.so.*

%post -n libcephfs_jni1 -p /sbin/ldconfig

%postun -n libcephfs_jni1 -p /sbin/ldconfig

%files -n libcephfs_jni-devel
%{_libdir}/libcephfs_jni.so

%files -n cephfs-java
%{_javadir}/libcephfs.jar
%{_javadir}/libcephfs-test.jar
%endif

%files -n rados-objclass-devel
%dir %{_includedir}/rados
%{_includedir}/rados/objclass.h

%if 0%{with selinux}
%files selinux
%attr(0600,root,root) %{_datadir}/selinux/packages/ceph.pp
%{_datadir}/selinux/devel/include/contrib/ceph.if
%{_mandir}/man8/ceph_selinux.8*

%post selinux
# backup file_contexts before update
. /etc/selinux/config
FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

# Install the policy
/usr/sbin/semodule -i %{_datadir}/selinux/packages/ceph.pp

# Load the policy if SELinux is enabled
if ! /usr/sbin/selinuxenabled; then
    # Do not relabel if selinux is not enabled
    exit 0
fi

if diff ${FILE_CONTEXT} ${FILE_CONTEXT}.pre > /dev/null 2>&1; then
   # Do not relabel if file contexts did not change
   exit 0
fi

# Check whether the daemons are running
/usr/bin/systemctl status ceph.target > /dev/null 2>&1
STATUS=$?

# Stop the daemons if they were running
if test $STATUS -eq 0; then
    /usr/bin/systemctl stop ceph.target > /dev/null 2>&1
fi

# Relabel the files
# Use ceph-disk fix for first package install and fixfiles otherwise
if [ "$1" = "1" ]; then
    /usr/sbin/ceph-disk fix --selinux
else
    /usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null
fi

rm -f ${FILE_CONTEXT}.pre
# The fixfiles command won't fix label for /var/run/ceph
/usr/sbin/restorecon -R /var/run/ceph > /dev/null 2>&1

# Start the daemons iff they were running before
if test $STATUS -eq 0; then
    /usr/bin/systemctl start ceph.target > /dev/null 2>&1 || :
fi
exit 0

%postun selinux
if [ $1 -eq 0 ]; then
    # backup file_contexts before update
    . /etc/selinux/config
    FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
    cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

    # Remove the module
    /usr/sbin/semodule -n -r ceph > /dev/null 2>&1

    # Reload the policy if SELinux is enabled
    if ! /usr/sbin/selinuxenabled ; then
        # Do not relabel if SELinux is not enabled
        exit 0
    fi

    # Check whether the daemons are running
    /usr/bin/systemctl status ceph.target > /dev/null 2>&1
    STATUS=$?

    # Stop the daemons if they were running
    if test $STATUS -eq 0; then
        /usr/bin/systemctl stop ceph.target > /dev/null 2>&1
    fi

    /usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null
    rm -f ${FILE_CONTEXT}.pre
    # The fixfiles command won't fix label for /var/run/ceph
    /usr/sbin/restorecon -R /var/run/ceph > /dev/null 2>&1

    # Start the daemons if they were running before
    if test $STATUS -eq 0; then
	/usr/bin/systemctl start ceph.target > /dev/null 2>&1 || :
    fi
fi
exit 0

%endif # with selinux

%if 0%{with python2}
%files -n python-ceph-compat
# We need an empty %%files list for python-ceph-compat, to tell rpmbuild to
# actually build this meta package.
%endif


%changelog
