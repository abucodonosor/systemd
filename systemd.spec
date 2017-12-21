%ifarch %{ix86}
%define _disable_lto 1
%endif

%bcond_without bootstrap

# macros for sysvinit transition - should be equal to
# sysvinit %version-%release-plus-1
%define sysvinit_version 2.87
%define sysvinit_release %mkrel 23

%define libsystemd_major 0
%define libnss_major 2

%define libsystemd %mklibname %{name} %{libsystemd_major}
%define libsystemd_devel %mklibname %{name} -d

%define libnss_myhostname %mklibname nss_myhostname %{libnss_major}
%define libnss_mymachines %mklibname nss_mymachines %{libnss_major}
%define libnss_resolve %mklibname nss_resolve %{libnss_major}
%define libnss_systemd %mklibname nss_systemd %{libnss_major}

%define udev_major 1
%define libudev %mklibname udev %{udev_major}
%define libudev_devel %mklibname udev -d

%define systemd_libdir /lib/systemd
%define udev_libdir /lib/udev
%define udev_rules_dir %{udev_libdir}/rules.d
%define udev_user_rules_dir %{_sysconfdir}/udev/rules.d

Summary:	A System and Session Manager
Name:		systemd
Version:	236
Release:	1
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/systemd
Source0:	http://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.gz
Source2:	50-udev-mandriva.rules
Source3:	69-printeracl.rules
Source5:	udev.sysconfig
# (blino) net rules and helpers
Source6:	76-net.rules
Source7:	udev_net_create_ifcfg
Source8:	udev_net_action
Source9:	udev_net.sysconfig
# (hk) udev rules for zte 3g modems with drakx-net
Source10:	61-mobile-zte-drakx-net.rules
Source11:	listen.conf
# (tpg) default preset for services
Source12:	99-default-disable.preset
Source13:	90-default.preset
Source14:	85-display-manager.preset
Source16:	systemd.rpmlintrc
# (tpg) by default enable network on eth, enp0s3
Source17:	90-enable.network
Source18:	90-user-default.preset
Source19:	10-imx.rules
Source20:	90-wireless.network
# (tpg) EFI bootctl
Source21:	efi-loader.conf
Source22:	efi-omv.conf

Source23:	systemd-udev-trigger-no-reload.conf
### OMV patches###
# Without this, build fails on aarch64
# (tpg) let's disable it for now
#Patch1:		systemd-233-format-nonliteral-warnings.patch
# from Mandriva
# disable coldplug for storage and device pci (nokmsboot/failsafe boot option required for proprietary video driver handling)
#po 315
Patch2:		0503-Disable-modprobe-pci-devices-on-coldplug-for-storage.patch
Patch5:		systemd-216-set-udev_log-to-err.patch
Patch8:		systemd-206-set-max-journal-size-to-150M.patch
Patch11:	systemd-220-silent-fsck-on-boot.patch
Patch14:	systemd-217-do-not-run-systemd-firstboot-in-containers.patch
Patch15:	1005-create-default-links-for-primary-cd_dvd-drive.patch
Patch17:	0515-Add-path-to-locale-search.patch
Patch18:	0516-udev-silence-version-print.patch
Patch20:	systemd-236-fix-build-with-LLVM.patch

# (tpg) ClearLinux patches
Patch100:	0001-journal-raise-compression-threshold.patch
Patch101:	0002-journal-clearout-drop-kmsg.patch
Patch102:	0003-core-use-mmap-to-load-files.patch
Patch103:	0005-journal-flush-var-kmsg-after-starting.patch
Patch104:	0010-sd-event-return-malloc-memory-reserves-when-main-loo.patch
Patch105:	0020-tmpfiles-Make-var-cache-ldconfig-world-readable.patch
Patch106:	0024-more-udev-children-workers.patch
Patch107:	0029-Enable-BBR-Bottleneck-Bandwidth-and-RTT.patch
Patch108:	0030-network-online-complete-once-one-link-is-online-not-.patch
Patch109:	0031-DHCP-retry-faster.patch
Patch110:	0033-Remove-libm-memory-overhead.patch
Patch111:	0035-skip-not-present-ACPI-devices.patch
Patch112:	0038-Compile-udev-with-O3.patch
Patch113:	0039-Don-t-wait-for-utmp-at-shutdown.patch
Patch114:	0040-network-wait-online-don-t-pass-NULL-to-strv_find.patch

BuildRequires:	meson
BuildRequires:	quota
BuildRequires:	acl-devel
BuildRequires:	audit-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-dtd45-xml
BuildRequires:	gperf
BuildRequires:	intltool
BuildRequires:	cap-devel
BuildRequires:	pam-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	tcp_wrappers-devel
BuildRequires:	elfutils-devel
BuildRequires:	pkgconfig(dbus-1) >= 1.12.2
BuildRequires:	pkgconfig(gee-0.8)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	gtk-doc
%if !%{with bootstrap}
BuildRequires:	pkgconfig(libcryptsetup)
BuildRequires:	pkgconfig(python)
%endif
BuildRequires:	pkgconfig(libkmod) >= 5
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(libqrencode)
BuildRequires:	pkgconfig(libiptc)
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(blkid) >= 2.30
BuildRequires:	usbutils >= 005-3
BuildRequires:	pciutils-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(liblz4)
%ifnarch %armx
BuildRequires:	valgrind-devel
BuildRequires:	gnu-efi
%if !%{with bootstrap}
BuildRequires:	qemu
%endif
%endif
BuildRequires:	chkconfig
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libidn)
BuildRequires:	pkgconfig(polkit-gobject-1)
#BuildRequires:	apparmor-devel
# To make sure _rundir is defined
BuildRequires:  rpm-build >= 1:5.4.10-79
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(mount) >= 2.27
# make sure we have /etc/os-release available, required by --with-distro
BuildRequires:	distro-release-common >= 2012.0-0.4
%if !%{with bootstrap}
BuildRequires:	pkgconfig(gobject-introspection-1.0)
%endif
Requires:	acl
Requires:	dbus >= 1.12.2
Requires(post):	coreutils >= 8.28
Requires(post):	gawk
Requires(post):	awk
Requires(post):	grep
Requires(post):	awk
Requires:	basesystem-minimal >= 1:3-1
Requires:	util-linux >= 2.27
Requires:	shadow >= 4.5.1
Requires(post,postun):	setup >= 2.8.9
Requires:	kmod >= 24
Conflicts:	initscripts < 9.24
Conflicts:	udev < 221-1
%if "%{distepoch}" >= "2013.0"
#(tpg) time to drop consolekit stuff as it is replaced by native logind
Provides:	consolekit = 0.4.5-6
Provides:	consolekit-x11 = 0.4.5-6
Obsoletes:	consolekit <= 0.4.5-5
Obsoletes:	consolekit-x11 <= 0.4.5-5
Obsoletes:	libconsolekit0
Obsoletes:	lib64consolekit0
%endif
%if "%{distepoch}" >= "2015.0"
# (tpg) this is obsoleted
Obsoletes:	suspend < 1.0-10
Provides:	suspend = 1.0-10
Obsoletes:	suspend-s2ram < 1.0-10
Provides:	suspend-s2ram = 1.0-10
%endif
Provides:	should-restart = system
# (tpg) just to be sure we install this libraries
Requires:	%{libsystemd} = %{EVRD}
Requires:	%{libnss_myhostname} = %{EVRD}
Requires:	%{libnss_resolve} = %{EVRD}
Requires:	%{libnss_systemd} = %{EVRD}
Suggests:	%{name}-boot
Suggests:	%{name}-console
Suggests:	%{name}-coredump
Suggests:	%{name}-doc
Suggests:	%{name}-hwdb
Suggests:	%{name}-locale
Suggests:	%{name}-polkit
Suggests:	%{name}-bash-completion = %{EVRD}
Suggests:	%{name}-zsh-completion = %{EVRD}

#(tpg)for future releases... systemd provides also a full functional syslog tool
Provides:	syslog-daemon
# (tpg) conflict with old sysvinit subpackage
%rename		systemd-sysvinit
Conflicts:	systemd-sysvinit < 207-1
# (eugeni) systemd should work as a drop-in replacement for sysvinit, but not obsolete it
#SysVinit < %sysvinit_release-%sysvinit_release It's provides something
#like that SysVinit < 14-14 when it should be SysVinit 2.87-14
Provides:	sysvinit = %sysvinit_version-%sysvinit_release, SysVinit = %sysvinit_version-%sysvinit_release
# (tpg) time to die
Obsoletes:	sysvinit < %sysvinit_version-%sysvinit_release, SysVinit < %sysvinit_version-%sysvinit_release
# Due to halt/poweroff etc. in _bindir
Conflicts:	usermode-consoleonly < 1:1.110
Obsoletes:	hal <= 0.5.14-6
# (tpg) moved form makedev package
Provides:	dev
Obsoletes:	MAKEDEV < 4.4-23
Provides:	MAKEDEV = 4.4-23
Conflicts:	makedev < 4.4-23
Obsoletes:	readahead < 1.5.7-8
Provides:	readahead = 1.5.7-8
Obsoletes:	resolvconf < 1.75-3
Provides:	resolvconf = 1.75-3
Obsoletes:	bootchart < 2.0.11.4-3
Provides:	bootchart = 2.0.11.4-3
Obsoletes:	python-%{name} < 223
Provides:	python-%{name} = 223
Obsoletes:	gummiboot
%rename		systemd-tools
%rename		systemd-units
%rename		udev

%description
systemd is a system and session manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package boot
Summary:	EFI boot component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9
Suggests:	%{name}-doc = %{EVRD}
Suggests:	%{name}-locale = %{EVRD}

%description boot
Systemd boot tools to manage EFI boot.

%package console
Summary:	Console support for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9
Suggests:	%{name}-doc = %{EVRD}
Suggests:	%{name}-locale = %{EVRD}

%description console
Some systemd units and udev rules are useful only when
you have an actual console, this subpackage contains
these units.

%package coredump
Summary:	Coredump component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9
Suggests:	%{name}-doc = %{EVRD}
Suggests:	%{name}-locale = %{EVRD}
Suggests:	gdb

%description coredump
Systemd coredump tools to manage coredumps and backtraces.

%package doc
Summary:	Man pages and documentation for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9
Suggests:	%{name}-locale = %{EVRD}

%description doc
Man pages and documentation for %{name}.

%package hwdb
Summary:	hwdb component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9
Suggests:	%{name}-polkit = %{EVRD}
Suggests:	%{name}-doc = %{EVRD}
Suggests:	%{name}-locale = %{EVRD}

%description hwdb
Hardware database management tool for %{name}.

%package locale
Summary:	Translations component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9

%description locale
Translations for %{name}.

%package polkit
Summary:	PolKit component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9

%description polkit
PolKit support for %{name}.

%package container
Summary:	Tools for containers and VMs
Group:		System/Base
Requires:	%{name} = %{EVRD}
Requires:	%{libnss_mymachines} = %{EVRD}
Conflicts:	%{name} < 235-1
Suggests:	%{name}-polkit = %{EVRD}
Suggests:	%{name}-bash-completion = %{EVRD}
Suggests:	%{name}-zsh-completion = %{EVRD}

%description container
Systemd tools to spawn and manage containers and virtual machines.
This package contains systemd-nspawn, machinectl, systemd-machined,
and systemd-importd.

%package journal-gateway
Summary:	Gateway for serving journal events over the network using HTTP
Group:		System/Configuration/Boot and Init
Requires:	%{name} = %{EVRD}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Obsoletes:	systemd < 206-7

%description journal-gateway
Offers journal events over the network using HTTP.

%package -n %{libsystemd}
Summary:	Systemdlibrary package
Group:		System/Libraries
# (tpg) old, pre 230 stuff - keep for smooth update from old relases
Provides:	libsystemd = 208-20
Obsoletes:	libsystemd < 208-20
Provides:	libsystemd-daemon = 208-20
Obsoletes:	libsystemd-daemon < 208-20
%rename		%{_lib}systemd-daemon0
Provides:	libsystemd-login = 208-20
Obsoletes:	libsystemd-login < 208-20
%rename		%{_lib}systemd-login0
Provides:	libsystemd-journal = 208-20
Obsoletes:	libsystemd-journal < 208-20
%rename		%{_lib}systemd-journal0
%rename		%{_lib}systemd-id1280
Obsoletes:	libsystemd-id1280 < 208-20
Provides:	libsystemd-id1280 = 208-20
%rename		%{_lib}systemd-id128_0

%description -n	%{libsystemd}
This package provides the systemd shared library.

%package -n %{libsystemd_devel}
Summary:	Systemd library development files
Group:		Development/C
Requires:	%{libsystemd} = %{EVRD}
# (tpg) old, pre 230 stuff - keep for smooth update from old relases
%rename		%{_lib}systemd-daemon0-devel
%rename		%{_lib}systemd-daemon-devel
%rename		%{_lib}systemd-login0-devel
%rename		%{_lib}systemd-login-devel
%rename		%{_lib}systemd-journal0-devel
%rename		%{_lib}systemd-journal-devel
%rename		%{_lib}systemd-id1280-devel
%rename		%{_lib}systemd-id128-devel

%description -n	%{libsystemd_devel}
Development files for the systemd shared library.

%package -n %{libnss_myhostname}
Summary:	Library for local system host name resolution
Group:		System/Libraries
Provides:	libnss_myhostname = %{EVRD}
Provides:	nss_myhostname = %{EVRD}
# (tpg) fix update from 2014.0
Provides:	nss_myhostname = 208-20
Obsoletes:	nss_myhostname < 208-20
Requires(post,preun):	/bin/sh
Requires(post,preun):	sed
Requires(post,preun):	glibc

%description -n %{libnss_myhostname}
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2).

%package -n %{libnss_mymachines}
Summary:	Provide hostname resolution for local container instances
Group:		System/Libraries
Provides:	libnss_mymachines = %{EVRD}
Provides:	nss_mymachines = %{EVRD}
Conflicts:	%{libnss_myhostname} < 235
Requires:	systemd-container = %{EVRD}
Requires(post,preun):	/bin/sh
Requires(post,preun):	sed
Requires(post,preun):	glibc

%description -n %{libnss_mymachines}
nss-mymachines is a plug-in module for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc), providing hostname resolution
for the names of containers running locally that are registered with 
systemd-machined.service(8). The container names are resolved to the IP 
addresses of the specific container, ordered by their scope. 
This functionality only applies to containers using network namespacing.

%package -n %{libnss_resolve}
Summary:	Provide hostname resolution via systemd-resolved.service
Group:		System/Libraries
Provides:	libnss_resolve = %{EVRD}
Provides:	nss_resolve= %{EVRD}
Conflicts:	%{libnss_myhostname} < 235
Requires(post,preun):	/bin/sh
Requires(post,preun):	sed
Requires(post,preun):	glibc

%description -n %{libnss_resolve}
nss-resolve is a plug-in module for the GNU Name Service Switch (NSS) 
functionality of the GNU C Library (glibc) enabling it to resolve host 
names via the systemd-resolved(8) local network name resolution service. 
It replaces the nss-dns plug-in module that traditionally resolves 
hostnames via DNS.

%package -n %{libnss_systemd}
Summary:	Provide UNIX user and group name resolution for dynamic users and groups
Group:		System/Libraries
Provides:	libnss_systemd = %{EVRD}
Provides:	nss_systemd = %{EVRD}
Conflicts:	%{libnss_myhostname} < 235
Requires(post,preun):	/bin/sh
Requires(post,preun):	sed
Requires(post,preun):	glibc

%description -n %{libnss_resolve}
nss-systemd is a plug-in module for the GNU Name Service Switch (NSS) 
functionality of the GNU C Library (glibc), providing UNIX user and 
group name resolution for dynamic users and groups allocated through 
the DynamicUser= option in systemd unit files. See systemd.exec(5) 
for details on this option.

%package -n %{libudev}
Summary:	Library for udev
Group:		System/Libraries
Obsoletes:	%{mklibname hal 1} <= 0.5.14-6

%description -n	%{libudev}
Library for udev.

%package -n %{libudev_devel}
Summary:	Devel library for udev
Group:		Development/C
License:	LGPLv2+
Provides:	udev-devel = %{EVRD}
Requires:	%{libudev} = %{EVRD}
Obsoletes:	%{_lib}udev0-devel
Obsoletes:	%{name}-doc

%description -n	%{libudev_devel}
Devel library for udev.

%package -n udev-doc
Summary:	Udev documentation
Group:		Books/Computer books

%description -n	udev-doc
This package contains documentation of udev.

%package	zsh-completion
Summary:	zsh completions
Group:	Shells
Requires:	zsh

%description	zsh-completion
This package contains zsh completion.

%package	bash-completion
Summary:	bash completions
Group:	Shells
Requires:	bash

%description	bash-completion
This package contains bash completion.

%prep
%setup -q
%apply_patches

%build
%ifarch %{ix86}
# (tpg) since LLVM/clang-3.8.0 systemd hangs system on i586
# (bero) since 3.9.0, also hangs system on x86_64
export CC=gcc
export CXX=g++
%endif

%serverbuild_hardened
%meson \
	-Drootprefix="" \
	-Drootlibdir=/%{_lib} \
	-Dlibexecdir=%{_prefix}/lib \
	-Dsysvinit-path=%{_initrddir} \
	-Dsysvrcnd-path=%{_sysconfdir}/rc.d \
	-Drc-local=/etc/rc.d/rc.local \
%ifnarch %armx
	-Dgnu-efi=true \
%endif
%if %{with bootstrap}
	-Dlibcryptsetup=false \
%endif
	-Dsplit-usr=true \
	-Dxkbcommon=true \
	-Dtpm=true \
	-Ddev-kvm-mode=0666 \
	-Dkmod=true \
	-Dxkbcommon=true \
	-Dblkid=true \
	-Dseccomp=true \
	-Dima=true \
	-Dselinux=false \
	-Dapparmor=false \
	-Dpolkit=true \
	-Dxz=true \
	-Dzlib=true \
	-Dbzip2=true \
	-Dlz4=true \
	-Dpam=true \
	-Dacl=true \
	-Dsmack=true \
	-Dgcrypt=true \
	-Daudit=true \
	-Delfutils=true \
	-Dqrencode=true \
	-Dgnutls=true \
	-Dmicrohttpd=true \
	-Dlibidn=true \
	-Dlibiptc=true \
	-Dlibcurl=true \
	-Dtpm=true \
	-Dhwdb=true \
	-Dsysusers=true \
	-Ddefault-kill-user-processes=false \
	-Dtests=unsafe \
	-Dinstall-tests=false \
%ifnarch %{ix86}
	-Db_lto=true \
%else
	-Db_lto=false \
%endif
	-Dloadkeys-path=/bin/loadkeys \
	-Dsetfont-path=/bin/setfont \
	-Dcertificate-root="%{_sysconfdir}/pki" \
	-Dfallback-hostname=openmandriva \
	-Dsupport-url="%{disturl}" \
%if %mdvver <= 3000000
	-Ddefault-hierarchy=hybrid \
%else
	-Ddefault-hierarchy=unified \
%endif
	-Dsystem-uid-max='999' \
	-Dsystem-gid-max='999' \
	-Dntp-servers='0.openmandriva.pool.ntp.org 1.openmandriva.pool.ntp.org 2.openmandriva.pool.ntp.org 3.openmandriva.pool.ntp.org' \
	-Ddns-servers='208.67.222.222 208.67.220.220'

%meson_build

%install
%meson_install

mkdir -p %{buildroot}{/bin,%{_sbindir}}

# (bor) create late shutdown and sleep directory
mkdir -p %{buildroot}%{systemd_libdir}/system-shutdown
mkdir -p %{buildroot}%{systemd_libdir}/system-sleep

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
mkdir -p %{buildroot}/sbin
ln -s ..%{systemd_libdir}/%{name} %{buildroot}/sbin/init
ln -s ..%{systemd_libdir}/%{name} %{buildroot}/bin/%{name}

# (tpg) install compat symlinks
for i in halt poweroff reboot; do
    ln -s /bin/systemctl %{buildroot}/bin/$i
done

for i in runlevel shutdown telinit; do
    ln -s ../bin/systemctl %{buildroot}/sbin/$i
done

ln -s /bin/loginctl %{buildroot}%{_bindir}/%{name}-loginctl

# (tpg) dracut needs this
ln -s /bin/systemctl %{buildroot}%{_bindir}/systemctl

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
rm -r %{buildroot}%{_sysconfdir}/%{name}/system/*.target.wants

# Make sure these directories are properly owned
mkdir -p %{buildroot}/%{systemd_libdir}/system/basic.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/default.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/dbus.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/syslog.target.wants
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/system/getty.target.wants

# And the default symlink we generate automatically based on inittab
rm -f %{buildroot}%{_sysconfdir}/%{name}/system/default.target

# (tpg) this is needed
mkdir -p %{buildroot}%{_prefix}/lib/%{name}/system-generators
mkdir -p %{buildroot}%{_prefix}/lib/%{name}/user-generators

# (bor) make sure we own directory for bluez to install service
mkdir -p %{buildroot}/%{systemd_libdir}/system/bluetooth.target.wants

# (tpg) use systemd's own mounting capability
sed -i -e 's/^#MountAuto=yes$/MountAuto=yes/' %{buildroot}/etc/%{name}/system.conf
sed -i -e 's/^#SwapAuto=yes$/SwapAuto=yes/' %{buildroot}/etc/%{name}/system.conf

# (bor) enable rpcbind.target by default so we have something to plug portmapper service into
ln -s ../rpcbind.target %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants

# (tpg) explicitly enable these services
ln -sf /lib/%{name}/system/%{name}-resolved.service %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants/%{name}-resolved.service
ln -sf /lib/%{name}/system/%{name}-networkd.service %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants/%{name}-networkd.service
ln -sf /lib/%{name}/system/%{name}-timesyncd.service %{buildroot}/%{systemd_libdir}/system/sysinit.target.wants/%{name}-timesyncd.service

# (eugeni) install /run
mkdir %{buildroot}/run

# (tpg) create missing dir
mkdir -p %{buildroot}%{_libdir}/%{name}/user/
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/user/default.target.wants

# Create new-style configuration files so that we can ghost-own them
touch %{buildroot}%{_sysconfdir}/hostname
touch %{buildroot}%{_sysconfdir}/vconsole.conf
touch %{buildroot}%{_sysconfdir}/locale.conf
touch %{buildroot}%{_sysconfdir}/machine-id
touch %{buildroot}%{_sysconfdir}/machine-info
touch %{buildroot}%{_sysconfdir}/timezone
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d
touch %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
mkdir -p %{buildroot}%{_sysconfdir}/udev
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin

# (cg) Set up the pager to make it generally more useful
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh << EOF
export SYSTEMD_PAGER="/usr/bin/less -FR"
EOF
chmod 644 %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh

# (tpg) move to etc
mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
mv -f %{buildroot}%{_prefix}/lib/rpm/macros.d/macros.systemd %{buildroot}%{_sysconfdir}/rpm/macros.d/systemd.macros

# Install logdir for journald
install -m 0755 -d %{buildroot}%{_logdir}/journal

#
install -m 0755 -d %{buildroot}%{_sysconfdir}/%{name}/network

# (tpg) Install default distribution preset policy for services
mkdir -p %{buildroot}%{systemd_libdir}/system-preset
# (tpg) add local user preset dir
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/user-preset
# (tpg) add global user preset dir
mkdir -p %{buildroot}%{_prefix}/lib/%{name}/user-preset

# (tpg) install presets
install -m 0644 %{SOURCE12} %{buildroot}%{systemd_libdir}/system-preset/
install -m 0644 %{SOURCE13} %{buildroot}%{systemd_libdir}/system-preset/
install -m 0644 %{SOURCE14} %{buildroot}%{systemd_libdir}/system-preset/

# (tpg) install network file
install -m 0644 %{SOURCE17} %{buildroot}%{systemd_libdir}/network/
# (fedya) install wireless file
install -m 0644 %{SOURCE20} %{buildroot}%{systemd_libdir}/network/

# (tpg) install userspace presets
install -m 0644 %{SOURCE18} %{buildroot}%{_prefix}/lib/%{name}/user-preset/

# Install rsyslog fragment
mkdir -p %{buildroot}%{_sysconfdir}/rsyslog.d/
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/rsyslog.d/

# (tpg) silent kernel messages
# print only KERN_ERR and more serious alerts
echo "kernel.printk = 3 3 3 3" >> %{buildroot}/usr/lib/sysctl.d/50-default.conf

# (tpg) by default enable SysRq
sed -i -e 's/^#kernel.sysrq = 0/kernel.sysrq = 1/' %{buildroot}/usr/lib/sysctl.d/50-default.conf

# (tpg) use 100M as a default maximum value for journal logs
sed -i -e 's/^#SystemMaxUse=.*/SystemMaxUse=100M/' %{buildroot}%{_sysconfdir}/%{name}/journald.conf

%ifnarch %armx
install -m644 -D %{SOURCE21} %{buildroot}%{_datadir}/%{name}/bootctl/loader.conf
install -m644 -D %{SOURCE22} %{buildroot}%{_datadir}/%{name}/bootctl/omv.conf
%endif

#################
#	UDEV	#
#	START	#
#################

install -m 644 %{SOURCE2} %{buildroot}%{udev_rules_dir}/
install -m 644 %{SOURCE3} %{buildroot}%{udev_rules_dir}/
mkdir -p  %{buildroot}%{_sysconfdir}/sysconfig/udev
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/udev/

# net rules
install -m 0644 %{SOURCE6} %{buildroot}%{udev_rules_dir}/
install -m 0755 %{SOURCE7} %{buildroot}%{udev_libdir}/net_create_ifcfg
install -m 0755 %{SOURCE8} %{buildroot}%{udev_libdir}/net_action
install -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/sysconfig/udev_net

install -m 0644 %{SOURCE10} %{buildroot}%{udev_rules_dir}/
install -m 0644 %{SOURCE19} %{buildroot}%{udev_rules_dir}/

# probably not required, but let's just be on the safe side for now..
ln -sf /bin/udevadm %{buildroot}/sbin/udevadm
ln -sf /bin/udevadm %{buildroot}%{_bindir}/udevadm
ln -sf /bin/udevadm %{buildroot}%{_sbindir}/udevadm

# (tpg) this is needed, because udevadm is in /bin
# altering the path allows to boot on before root pivot
sed -i --follow-symlinks -e 's#/bin/udevadm#/sbin/udevadm#g' %{buildroot}/%{systemd_libdir}/system/*.service

mkdir -p %{buildroot}%{_prefix}/lib/firmware/updates
mkdir -p %{buildroot}%{_sysconfdir}/udev/agents.d/usb
touch %{buildroot}%{_sysconfdir}/scsi_id.config

ln -s ..%{systemd_libdir}/%{name}-udevd %{buildroot}/sbin/udevd
ln -s %{systemd_libdir}/%{name}-udevd %{buildroot}%{udev_libdir}/udevd

# udev rules for zte 3g modems and drakx-net

mkdir -p %{buildroot}/lib/firmware/updates
# default /dev content, from Fedora RPM
mkdir -p %{buildroot}%{udev_libdir}/devices/{net,hugepages,pts,shm}
# From previous Mandriva /etc/udev/devices.d
mkdir -p %{buildroot}%{udev_libdir}/devices/cpu/0

#################
#	UDEV	#
#	END	#
#################

# (tpg) just delete this for now
# file /usr/share/man/man5/crypttab.5.xz 
# from install of systemd-186-2.x86_64
# conflicts with file from package initscripts-9.25-10.x86_64
rm -rf %{buildroot}%{_mandir}/man5/crypttab*

# https://bugzilla.redhat.com/show_bug.cgi?id=1378974
install -Dm0644 -t %{buildroot}%{systemd_libdir}/system/systemd-udev-trigger.service.d/ %{SOURCE23}

# Pre-generate and pre-ship hwdb, to speed up first boot
./build/systemd-hwdb --root %{buildroot} --usr update || ./build/udevadm hwdb --root %{buildroot} --update --usr

# Compute catalog
./build/journalctl --root %{buildroot} --update-catalog

%find_lang %{name}

%triggerin -- glibc
# reexec daemon on self or glibc update to avoid busy / on shutdown
# trigger is executed on both self and target install so no need to have
# extra own post
if [ $1 -ge 2 -o $2 -ge 2 ] ; then
    /bin/systemctl daemon-reexec 2>&1 || :
fi

%pre
if [ $1 -ge 2 ]; then
    systemctl stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service >/dev/null 2>&1 || :
fi

%post
/bin/systemd-firstboot --setup-machine-id >/dev/null 2>&1 ||:
/bin/systemd-sysusers >/dev/null 2>&1 ||:
/bin/systemd-machine-id-setup >/dev/null 2>&1 ||:
%{systemd_libdir}/systemd-random-seed save >/dev/null 2>&1 || :
/bin/systemctl daemon-reexec >/dev/null 2>&1 || :
/bin/systemctl start systemd-udevd.service >/dev/null 2>&1 || :
/bin/systemd-hwdb update >/dev/null 2>&1 || :
/bin/journalctl --update-catalog >/dev/null 2>&1 || :

# (tpg) move sysctl.conf to /etc/sysctl.d as since 207 /etc/sysctl.conf is skipped
if [ $1 -ge 2 ]; then
    if [ -e %{_sysconfdir}/sysctl.conf ] && [ ! -L %{_sysconfdir}/sysctl.conf ]; then
	mv -f %{_sysconfdir}/sysctl.conf %{_sysconfdir}/sysctl.d/99-sysctl.conf
	ln -s %{_sysconfdir}/sysctl.d/99-sysctl.conf %{_sysconfdir}/sysctl.conf
    fi
fi

# (tpg) from old units package
if [ $1 -eq 2 ] ; then
    # Try to read default runlevel from the old inittab if it exists
    runlevel=$(/bin/awk -F ':' '$3 == "initdefault" && $1 !~ "^#" { print $2 }' /etc/inittab 2> /dev/null)
    if [ -z "$runlevel" ] ; then
	target="/lib/systemd/system/graphical.target"
    else
	target="/lib/systemd/system/runlevel$runlevel.target"
    fi
# And symlink what we found to the new-style default.target
    /bin/ln -sf "$target" %{_sysconfdir}/systemd/system/default.target 2>&1 || :
fi

# Enable the services we install by default.
/bin/systemctl preset-all &>/dev/null || :

hostname_new=`cat %{_sysconfdir}/hostname 2>/dev/null`
if [ -z $hostname_new ]; then
    hostname_old=`cat /etc/sysconfig/network 2>/dev/null | grep HOSTNAME | cut -d "=" -f2`
    if [ ! -z $hostname_old ]; then
	echo $hostname_old >> %{_sysconfdir}/hostname
    else
	echo "localhost" >> %{_sysconfdir}/hostname
    fi
fi

# Remove spurious /etc/fstab entries from very old installations
if [ -e /etc/fstab ]; then
    grep -v -E -q '^(devpts|tmpfs|sysfs|proc)' /etc/fstab || \
	sed -i.rpm.bak -r '/^devpts\s+\/dev\/pts\s+devpts\s+defaults\s+/d; /^tmpfs\s+\/dev\/shm\s+tmpfs\s+defaults\s+/d; /^sysfs\s+\/sys\s+sysfs\s+defaults\s+/d; /^proc\s+\/proc\s+proc\s+defaults\s+/d' /etc/fstab || :
fi

# (tpg) create resolv.conf based on systemd
if [ $1 -ge 1 ]; then
    if [ ! -e /run/systemd/resolve/resolv.conf ]; then
	mkdir -p /run/systemd/resolve
	echo -e "nameserver 208.67.222.222\nnameserver 208.67.220.220\n" > /run/systemd/resolve/resolv.conf
    fi
fi

# (tpg) link to resolv.conf from systemd
if [ $1 -eq 1 ]; then
    if [ -e /etc/resolv.conf ]; then
	rm -f /etc/resolv.conf
    fi
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
fi

# (tpg) on update always set to systemd resolv.conf
if [ $1 -ge 2 ]; then
    if [ -L /etc/resolv.conf ] && [ "$(readlink /etc/resolv.conf)" != "../run/systemd/resolve/resolv.conf" ]; then
	rm -f /etc/resolv.conf
	ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
    fi

    /bin/systemctl restart systemd-resolved.service 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    /bin/systemctl --quiet disable \
	    getty@tty1.service \
	    getty@getty.service \
	    remote-fs.target \
	    systemd-networkd.service \
	    systemd-resolvd.service \
	    systemd-timesync.service \
	    systemd-timedated.service \
	    console-getty.service \
	    console-shell.service \
	    debug-shell.service \
	    2>&1 || :

    /bin/rm -f /etc/systemd/system/default.target 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] ; then
    /bin/systemctl daemon-reload > /dev/null 2>&1 || :
fi

%triggerun -- %{name} < 208-2
chgrp -R systemd-journal /var/log/journal || :
chmod 02755 /var/log/journal || :
if [ -f /etc/machine-id ]; then
    chmod 02755 /var/log/journal/$(cat /etc/machine-id) || :
fi

%triggerposttransun -- resolvconf < 1.75-4
if [ -f /etc/resolv.conf ]; then
    rm -f /etc/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
elif [ ! -e /etc/resolv.conf ]; then
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
elif [ -L /etc/resolv.conf ] && [ "$(readlink /etc/resolv.conf)" = "/run/resolvconf/resolv.conf" ]; then
    rm -f /etc/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
elif [ -L /etc/resolv.conf ] && [ "$(readlink /etc/resolv.conf)" = "/run/NetworkManager/resolv.conf" ]; then
    rm -f /etc/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
fi

/bin/systemctl enable systemd-resolved.service 2>&1 || :
/bin/systemctl restart systemd-resolved.service 2>&1 || :

%triggerposttransin -- %{_tmpfilesdir}/*.conf
if [ $1 -eq 1 -o $2 -eq 1 ]; then
    while [ -n "$3" ]; do
	if [ -f "$3" ]; then
	    /bin/systemd-tmpfiles --create "$3"
        fi
        shift
    done
fi

%triggerposttransun -- %{_tmpfilesdir}/*.conf
if [ $2 -eq 0 ]; then
    while [ -n "$3" ]; do
	if [ -f "$3" ]; then
            /bin/systemd-tmpfiles --remove "$3"
        fi
        shift
    done
fi

%triggerin -- %{name}-units < 217-10
# make sure we use preset here
/bin/systemctl --quiet preset \
	getty@getty.service \
	remote-fs.target \
	systemd-readahead-replay.service \
	systemd-readahead-collect.service \
	console-getty.service \
	console-shell.service \
	debug-shell.service \
	2>&1 || :

/bin/systemctl --quiet stop getty@getty.service 2>&1 || :
/bin/systemctl --quiet disable getty@getty.service 2>&1 || :
/bin/systemctl --quiet stop systemd-readahead-replay.service 2>&1 || :
/bin/systemctl --quiet stop systemd-readahead-collect.service 2>&1 || :
/bin/systemctl --quiet disable systemd-readahead-replay.service 2>&1 || :
/bin/systemctl --quiet disable systemd-readahead-collect.service 2>&1 || :

%triggerpostun -- %{name}-units < 217-10
# remove wrong getty target
if [ -d %{_sysconfdir}/systemd/system/getty.target.wants/getty@getty.service ]
    /bin/systemctl --quiet disable getty@getty.service  2>&1 || :
    rm -rf %{_sysconfdir}/systemd/system/getty.target.wants ||:
fi

%triggerin -- ^%{_unitdir}/.*\.(service|socket|path|timer)$
ARG1=$1
ARG2=$2
shift
shift

units=${*#%{_unitdir}/}
if [ $ARG1 -eq 1 -a $ARG2 -eq 1 ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    /bin/systemctl preset ${units} >/dev/null 2>&1 || :
fi

%triggerun -- ^%{_unitdir}/.*\.(service|socket|path|timer)$
ARG1=$1
ARG2=$2
shift
shift

skip="$(grep -l 'Alias=display-manager.service' $*)"
units=${*#%{_unitdir}/}
units=${units#${skip##*/}}
if [ $ARG2 -eq 0 ]; then
    /bin/systemctl --no-reload disable ${units} >/dev/null 2>&1 || :
    /bin/systemctl stop ${units} >/dev/null 2>&1 || :
fi

%triggerpostun -- ^%{_unitdir}/.*\.(service|socket|path|timer)$
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%triggerposttransin -- %{_binfmtdir}/*.conf
/bin/systemctl reload-or-try-restart systemd-binfmt >/dev/null 2>&1 ||:

%triggerposttransun -- %{_binfmtdir}/*.conf
/bin/systemctl reload-or-try-restart systemd-binfmt >/dev/null 2>&1 ||:

%triggerposttransin -- /lib/udev/hwdb.d/*.hwdb
/bin/systemd-hwdb update >/dev/null 2>&1 ||:

%triggerposttransun -- /lib/udev/hwdb.d/*.hwdb
/bin/systemd-hwdb update >/dev/null 2>&1 ||:

%triggerposttransin -- %{udev_rules_dir}/*.rules
/sbin/udevadm control --reload >/dev/null 2>&1 ||:

%triggerposttransun -- %{udev_rules_dir}/*.rules
/sbin/udevadm control --reload >/dev/null 2>&1 ||:

%triggerposttransin -- %{udev_user_rules_dir}/*.rules
/sbin/udevadm control --reload >/dev/null 2>&1 ||:

%triggerposttransun -- %{udev_user_rules_dir}/*.rules
/sbin/udevadm control --reload >/dev/null 2>&1 ||:

%triggerposttransin -- %{_prefix}/lib/sysusers.d/*.conf
/bin/systemd-sysusers >/dev/null 2>&1 ||:

%triggerposttransun -- %{_prefix}/lib/sysusers.d/*.conf
/bin/systemd-sysusers >/dev/null 2>&1 ||:

%triggerposttransin -- %{_prefix}/lib/systemd/catalog/*.catalog
/bin/journalctl --update-catalog >/dev/null 2>&1 ||:

%triggerposttransun -- %{_prefix}/lib/systemd/catalog/*.catalog
/bin/journalctl --update-catalog >/dev/null 2>&1 ||:

%post -n %{libnss_myhostname}
if [ -f /etc/nsswitch.conf ]; then
# sed-fu to add myhostanme to hosts line
	grep -v -E -q '^hosts:.* myhostname' /etc/nsswitch.conf &&
	sed -i.bak -e '
		/^hosts:/ !b
		/\<myhostname\>/ b
		s/[[:blank:]]*$/ myhostname/
		' /etc/nsswitch.conf &>/dev/null || :
fi

%post -n %{libnss_mymachines}
if [ -f /etc/nsswitch.conf ]; then
	grep -E -q '^(passwd|group):.* mymachines' /etc/nsswitch.conf ||
	sed -i.bak -r -e '
		s/^(passwd|group):(.*)/\1: \2 mymachines/
		' /etc/nsswitch.conf &>/dev/null || :
fi
		
%postun -n %{libnss_mymachines}
# sed-fu to remove mymachines from passwd and group lines of /etc/nsswitch.conf
# https://bugzilla.redhat.com/show_bug.cgi?id=1284325
# To avoid the removal, e.g. add a space at the end of the line.
if [ -f /etc/nsswitch.conf ]; then
	grep -E -q '^(passwd|group):.* mymachines$' /etc/nsswitch.conf &&
	sed -i.bak -r -e '
		s/^(passwd:.*) mymachines$/\1/;
		s/^(group:.*) mymachines$/\1/;
		' /etc/nsswitch.conf &>/dev/null || :
fi

%post -n %{libnss_resolve}
if [ -f /etc/nsswitch.conf ]; then
	grep -E -q '^hosts:.*resolve[[:space:]]*($|[[:alpha:]])' /etc/nsswitch.conf &&
	sed -i.bak -e '
		/^hosts:/ { s/resolve/& [!UNAVAIL=return]/}
		' /etc/nsswitch.conf &>/dev/null || :
fi

%post -n %{libnss_systemd}
if [ -f /etc/nsswitch.conf ]; then
	grep -E -q '^(passwd|group):.* systemd' /etc/nsswitch.conf ||
	sed -i.bak -r -e '
		s/^(passwd|group):(.*)/\1: \2 systemd/
		' /etc/nsswitch.conf &>/dev/null || :
fi
		
%pre journal-gateway
%_pre_groupadd systemd-journal-gateway systemd-journal-gateway
%_pre_useradd systemd-journal-gateway %{_var}/log/journal /sbin/nologin
%_pre_groupadd systemd-journal-remote systemd-journal-remote
%_pre_useradd systemd-journal-remote %{_var}/log/journal/remote /sbin/nologin
%_pre_groupadd systemd-journal-upload systemd-journal-upload
%_pre_useradd systemd-journal-upload %{_var}/log/journal/upload /sbin/nologin

%files
%dir /lib/firmware
%dir /lib/firmware/updates
%dir /lib/modprobe.d
%dir %{_datadir}/factory
%dir %{_datadir}/factory/etc
%dir %{_datadir}/factory/etc/pam.d
%dir %{_datadir}/%{name}
%dir %{_prefix}/lib/binfmt.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/catalog
%dir %{_prefix}/lib/%{name}/system-generators
%dir %{_prefix}/lib/%{name}/user
%dir %{_prefix}/lib/%{name}/user-preset
%dir %{_prefix}/lib/%{name}/user-generators
%dir %{_prefix}/lib/systemd/user-environment-generators
%dir %{_prefix}/lib/sysusers.d
%dir %{_prefix}/lib/tmpfiles.d
%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/system
%dir %{_sysconfdir}/%{name}/system/getty.target.wants
%dir %{_sysconfdir}/%{name}/user
%dir %{_sysconfdir}/%{name}/user-preset
%dir %{_sysconfdir}/%{name}/user/default.target.wants
%dir %{_sysconfdir}/%{name}/network
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/agents.d
%dir %{_sysconfdir}/udev/agents.d/usb
%dir %{_sysconfdir}/udev/rules.d
%dir %{systemd_libdir}
%dir %{systemd_libdir}/*-generators
%dir %{systemd_libdir}/network
%dir %{systemd_libdir}/system
%dir %{systemd_libdir}/system-preset
%dir %{systemd_libdir}/system-shutdown
%dir %{systemd_libdir}/system-sleep
%dir %{systemd_libdir}/system/systemd-udev-trigger.service.d
%dir %{systemd_libdir}/system/basic.target.wants
%dir %{systemd_libdir}/system/bluetooth.target.wants
%dir %{systemd_libdir}/system/dbus.target.wants
%dir %{systemd_libdir}/system/default.target.wants
%dir %{systemd_libdir}/system/graphical.target.wants
%dir %{systemd_libdir}/system/local-fs.target.wants
%dir %{systemd_libdir}/system/multi-user.target.wants
%dir %{systemd_libdir}/system/rescue.target.wants
%dir %{systemd_libdir}/system/runlevel1.target.wants
%dir %{systemd_libdir}/system/runlevel2.target.wants
%dir %{systemd_libdir}/system/runlevel3.target.wants
%dir %{systemd_libdir}/system/runlevel4.target.wants
%dir %{systemd_libdir}/system/runlevel5.target.wants
%dir %{systemd_libdir}/system/sockets.target.wants
%dir %{systemd_libdir}/system/sysinit.target.wants
%dir %{systemd_libdir}/system/syslog.target.wants
%dir %{systemd_libdir}/system/timers.target.wants
%dir %{systemd_libdir}/system/machines.target.wants
%dir %{systemd_libdir}/system/remote-fs.target.wants
%dir %{udev_libdir}
%dir %{udev_libdir}/hwdb.d
%dir %{udev_rules_dir}
%dir %{_localstatedir}/lib/systemd
%dir %{_localstatedir}/lib/systemd/catalog
### container excludes
%exclude %{systemd_libdir}/system/dbus-org.freedesktop.import1.service
%exclude %{systemd_libdir}/system/dbus-org.freedesktop.machine1.service
%exclude %{systemd_libdir}/system/machine.slice
%exclude %{systemd_libdir}/system/machines.target
%exclude %{systemd_libdir}/system/machines.target.wants/var-lib-machines.mount
%exclude %{systemd_libdir}/system/remote-fs.target.wants/var-lib-machines.mount
%exclude %{systemd_libdir}/system/systemd-importd.service
%exclude %{systemd_libdir}/system/systemd-machined.service
%exclude %{systemd_libdir}/system/systemd-nspawn@.service
%exclude %{systemd_libdir}/system/var-lib-machines.mount
%exclude %{systemd_libdir}/systemd-import
%exclude %{systemd_libdir}/systemd-importd
%exclude %{systemd_libdir}/systemd-machined
%exclude %{systemd_libdir}/systemd-pull
%exclude %{systemd_libdir}/import-pubring.gpg
%exclude %{systemd_libdir}/systemd-import
%exclude %{systemd_libdir}/systemd-importd
%exclude %{systemd_libdir}/systemd-machined
%exclude %{systemd_libdir}/systemd-pull
%exclude %{systemd_libdir}/import-pubring.gpg
%exclude /bin/machinectl
%exclude %{_bindir}/systemd-nspawn
%exclude %{_prefix}/lib/tmpfiles.d/systemd-nspawn.conf
### gateway excludes
%exclude %{systemd_libdir}/system/%{name}-journal-gatewayd.service
%exclude %{systemd_libdir}/system/%{name}-journal-gatewayd.socket
%exclude %{systemd_libdir}/system/%{name}-journal-remote.service
%exclude %{systemd_libdir}/system/%{name}-journal-remote.socket
%exclude %{systemd_libdir}/system/%{name}-journal-upload.service
%exclude %{systemd_libdir}/%{name}-journal-gatewayd
%exclude %{systemd_libdir}/%{name}-journal-remote
%exclude %{systemd_libdir}/%{name}-journal-upload
%exclude %config(noreplace) %{_prefix}/lib/sysusers.d/%{name}-remote.conf
%exclude %config(noreplace) %{_sysconfdir}/%{name}/journal-remote.conf
%exclude %config(noreplace) %{_sysconfdir}/%{name}/journal-upload.conf
### console excludes
%exclude %{systemd_libdir}/systemd-vconsole-setup
%exclude %{systemd_libdir}/system/serial-getty@.service
%exclude %{udev_rules_dir}/90-vconsole.rules
%exclude %{udev_rules_dir}/70-mouse.rules
%exclude %{udev_rules_dir}/60-drm.rules
%exclude %{udev_rules_dir}/60-persistent-input.rules
%exclude %{udev_rules_dir}/70-touchpad.rules
%exclude %{udev_rules_dir}/60-evdev.rules
%exclude %{udev_rules_dir}/60-input-id.rules
### coredump excludes
%exclude %config(noreplace) %{_sysconfdir}/%{name}/coredump.conf
%exclude %{_prefix}/lib/sysctl.d/50-coredump.conf
%exclude %{systemd_libdir}/systemd-coredump
%exclude %{systemd_libdir}/system/systemd-coredump.socket
%exclude %{systemd_libdir}/system/systemd-coredump@.service
%exclude %{systemd_libdir}/system/sockets.target.wants/systemd-coredump.socket
### hwdb excludes
%exclude %{systemd_libdir}/system/sysinit.target.wants/systemd-hwdb-update.service
%exclude %{systemd_libdir}/system/systemd-hwdb-update.service
%exclude %{udev_rules_dir}/60-cdrom_id.rules
%exclude %{udev_rules_dir}/60-persistent-alsa.rules
%exclude %{udev_rules_dir}/60-persistent-storage-tape.rules
%exclude %{udev_rules_dir}/60-persistent-v4l.rules
%exclude %{udev_rules_dir}/70-joystick.rules
%exclude %{udev_rules_dir}/75-probe_mtd.rules
%exclude %{udev_rules_dir}/78-sound-card.rules
###
%ghost %config(noreplace,missingok) %attr(0644,root,root) %{_sysconfdir}/scsi_id.config
%ghost %config(noreplace) %{_sysconfdir}/hostname
%ghost %config(noreplace) %{_sysconfdir}/locale.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info
%ghost %config(noreplace) %{_sysconfdir}/timezone
%ghost %config(noreplace) %{_sysconfdir}/vconsole.conf
%ghost %config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.locale1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.login1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.network1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.timedate1.conf
/%{_lib}/security/pam_systemd.so
/bin/halt
/bin/journalctl
/bin/loginctl
/bin/networkctl
/bin/poweroff
/bin/reboot
/bin/systemctl
/bin/%{name}
/bin/%{name}-ask-password
/bin/%{name}-escape
/bin/%{name}-firstboot
/bin/%{name}-inhibit
/bin/%{name}-machine-id-setup
/bin/%{name}-notify
/bin/%{name}-sysusers
/bin/%{name}-tmpfiles
/bin/%{name}-tty-ask-password-agent
/bin/udevadm
/sbin/init
/sbin/runlevel
/sbin/shutdown
/sbin/telinit
%{_bindir}/busctl
%{_bindir}/hostnamectl
%{_bindir}/kernel-install
%{_bindir}/localectl
%{_bindir}/systemctl
%{_bindir}/%{name}-*
%{_bindir}/timedatectl
%{_sysconfdir}/systemd/system/dbus-org.freedesktop.network1.service
%{_sysconfdir}/systemd/system/dbus-org.freedesktop.resolve1.service
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.network1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.resolve1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service
%{_datadir}/factory/etc/nsswitch.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{_datadir}/%{name}/kbd-model-map
%{_datadir}/%{name}/language-fallback-map
%{_initrddir}/README
%{_logdir}/README
/lib/modprobe.d/systemd.conf
%{_prefix}/lib/kernel/install.d/*.install
%{_prefix}/lib/environment.d/99-environment.conf
%{_prefix}/lib/%{name}/user-preset/*.preset
%{_prefix}/lib/%{name}/user/*.service
%{_prefix}/lib/%{name}/user/*.target
%{_prefix}/lib/%{name}/user/*.timer
%{_prefix}/lib/systemd/user-environment-generators/*
%{_prefix}/lib/tmpfiles.d/*.conf
%{_sysconfdir}/profile.d/40systemd.sh
%{_sysconfdir}/rpm/macros.d/systemd.macros
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%{_sysconfdir}/xdg/%{name}
%{systemd_libdir}/resolv.conf
%{systemd_libdir}/*-generators/*
%{systemd_libdir}/network/80-container-host0.network
%{systemd_libdir}/network/80-container-ve.network
%{systemd_libdir}/network/80-container-vz.network
%{systemd_libdir}/network/90-enable.network
%{systemd_libdir}/network/90-wireless.network
%{systemd_libdir}/network/99-default.link
%{systemd_libdir}/system-preset/*.preset
%{systemd_libdir}/system/*.automount
%{systemd_libdir}/system/*.mount
%{systemd_libdir}/system/*.path
%{systemd_libdir}/system/*.service
%{systemd_libdir}/system/*.slice
%{systemd_libdir}/system/*.socket
%{systemd_libdir}/system/*.target
%{systemd_libdir}/system/*.timer
%{systemd_libdir}/system/systemd-udev-trigger.service.d/*.conf
%{systemd_libdir}/system/graphical.target.wants/*.service
%{systemd_libdir}/system/local-fs.target.wants/*.mount
%{systemd_libdir}/system/local-fs.target.wants/*.service
%{systemd_libdir}/system/multi-user.target.wants/*.path
%{systemd_libdir}/system/multi-user.target.wants/*.service
%{systemd_libdir}/system/multi-user.target.wants/*.target
%{systemd_libdir}/system/rescue.target.wants/*.service
%{systemd_libdir}/system/sockets.target.wants/*.socket
%{systemd_libdir}/system/sysinit.target.wants/*.*mount
%{systemd_libdir}/system/sysinit.target.wants/*.path
%{systemd_libdir}/system/sysinit.target.wants/*.service
%if !%{with bootstrap}
%{systemd_libdir}/system/sysinit.target.wants/*.target
%endif
%{systemd_libdir}/system/timers.target.wants/*.timer
%{systemd_libdir}/system/machines.target.wants/*.mount
%{systemd_libdir}/system/remote-fs.target.wants/*.mount
%{systemd_libdir}/systemd*
# (tpg) internal library - only systemd uses it
%{systemd_libdir}/libsystemd-shared-%{version}.so
#
%{udev_libdir}/*.bin
%{udev_rules_dir}/*.rules
%attr(02755,root,systemd-journal) %dir %{_logdir}/journal
%attr(0755,root,root) /sbin/udevadm
%attr(0755,root,root) /sbin/udevd
%attr(0755,root,root) %{_bindir}/udevadm
%attr(0755,root,root) %{_sbindir}/udevadm
%attr(0755,root,root) %{udev_libdir}/ata_id
%attr(0755,root,root) %{udev_libdir}/net_action
%attr(0755,root,root) %{udev_libdir}/net_create_ifcfg
%attr(0755,root,root) %{udev_libdir}/scsi_id
%attr(0755,root,root) %{udev_libdir}/udevd
%config(noreplace) %{_prefix}/lib/sysctl.d/*.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/*.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}-user
%config(noreplace) %{_sysconfdir}/rsyslog.d/listen.conf
%config(noreplace) %{_sysconfdir}/sysconfig/udev
%config(noreplace) %{_sysconfdir}/sysconfig/udev_net
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/udev/*.conf
%{_localstatedir}/lib/systemd/catalog/database

%files journal-gateway
%config(noreplace) %{_sysconfdir}/%{name}/journal-remote.conf
%config(noreplace) %{_sysconfdir}/%{name}/journal-upload.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/%{name}-remote.conf
%dir %{_datadir}/%{name}/gatewayd
%{systemd_libdir}/%{name}-journal-gatewayd
%{systemd_libdir}/%{name}-journal-remote
%{systemd_libdir}/%{name}-journal-upload
%{systemd_libdir}/system/%{name}-journal-gatewayd.service
%{systemd_libdir}/system/%{name}-journal-gatewayd.socket
%{systemd_libdir}/system/%{name}-journal-remote.service
%{systemd_libdir}/system/%{name}-journal-remote.socket
%{systemd_libdir}/system/%{name}-journal-upload.service
%{_datadir}/%{name}/gatewayd/browse.html

%files container
%{systemd_libdir}/system/dbus-org.freedesktop.import1.service
%{systemd_libdir}/system/dbus-org.freedesktop.machine1.service
%{systemd_libdir}/system/machine.slice
%{systemd_libdir}/system/machines.target
%{systemd_libdir}/system/machines.target.wants/var-lib-machines.mount
%{systemd_libdir}/system/remote-fs.target.wants/var-lib-machines.mount
%{systemd_libdir}/system/systemd-importd.service
%{systemd_libdir}/system/systemd-machined.service
%{systemd_libdir}/system/systemd-nspawn@.service
%{systemd_libdir}/system/var-lib-machines.mount
%{systemd_libdir}/systemd-import
%{systemd_libdir}/systemd-importd
%{systemd_libdir}/systemd-machined
%{systemd_libdir}/systemd-pull
%{systemd_libdir}/import-pubring.gpg
/bin/machinectl
%{_bindir}/systemd-nspawn
%{_prefix}/lib/tmpfiles.d/systemd-nspawn.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.import1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.import1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.machine1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.import1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.machine1.policy
	
%files -n %{libnss_mymachines}
/%{_lib}/libnss_mymachines.so.%{libnss_major}

%files -n %{libnss_myhostname}
/%{_lib}/libnss_myhostname.so.%{libnss_major}*

%files -n %{libnss_resolve}
/%{_lib}/libnss_resolve.so.%{libnss_major}

%files -n %{libnss_systemd}
/%{_lib}/libnss_systemd.so.%{libnss_major}

%files -n %{libsystemd}
/%{_lib}/libsystemd.so.%{libsystemd_major}*

%files -n %{libsystemd_devel}
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/_sd-common.h
%{_includedir}/%{name}/sd-bus-protocol.h
%{_includedir}/%{name}/sd-bus-vtable.h
%{_includedir}/%{name}/sd-bus.h
%{_includedir}/%{name}/sd-event.h
%{_includedir}/%{name}/sd-id128.h
%{_includedir}/%{name}/sd-journal.h
%{_includedir}/%{name}/sd-login.h
%{_includedir}/%{name}/sd-messages.h
%{_includedir}/%{name}/sd-daemon.h
/%{_lib}/lib%{name}.so
%{_datadir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/lib%{name}.pc

%files -n %{libudev}
/%{_lib}/libudev.so.%{udev_major}*

%files -n %{libudev_devel}
/%{_lib}/libudev.so
%{_libdir}/pkgconfig/libudev.pc
%{_datadir}/pkgconfig/udev.pc
%{_includedir}/libudev.h

%files boot
%{_bindir}/bootctl
%ifnarch %armx
%dir %{_prefix}/lib/%{name}/boot
%dir %{_prefix}/lib/%{name}/boot/efi
%dir %{_datadir}/%{name}/bootctl
%{_prefix}/lib/%{name}/boot/efi/*.efi
%{_prefix}/lib/%{name}/boot/efi/*.stub
%{_datadir}/%{name}/bootctl/*.conf
%endif

%files console
%{systemd_libdir}/systemd-vconsole-setup
%{systemd_libdir}/system/serial-getty@.service
%{udev_rules_dir}/90-vconsole.rules
%{udev_rules_dir}/70-mouse.rules
%{udev_rules_dir}/60-drm.rules
%{udev_rules_dir}/60-persistent-input.rules
%{udev_rules_dir}/70-touchpad.rules
%{udev_rules_dir}/60-evdev.rules
%{udev_rules_dir}/60-input-id.rules

%files coredump
%config(noreplace) %{_sysconfdir}/%{name}/coredump.conf
%{_bindir}/coredumpctl
%{_prefix}/lib/sysctl.d/50-coredump.conf
%{systemd_libdir}/systemd-coredump
%{systemd_libdir}/system/systemd-coredump.socket
%{systemd_libdir}/system/systemd-coredump@.service
%{systemd_libdir}/system/sockets.target.wants/systemd-coredump.socket

%files doc
%doc %{_docdir}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8.*

%files hwdb
%ghost %{_sysconfdir}/udev/hwdb.bin
%{systemd_libdir}/system/sysinit.target.wants/systemd-hwdb-update.service
%{systemd_libdir}/system/systemd-hwdb-update.service
/bin/systemd-hwdb
%{udev_libdir}/hwdb.d/*.hwdb
%{udev_rules_dir}/60-cdrom_id.rules
%{udev_rules_dir}/60-persistent-alsa.rules
%{udev_rules_dir}/60-persistent-storage-tape.rules
%{udev_rules_dir}/60-persistent-v4l.rules
%{udev_rules_dir}/70-joystick.rules
%{udev_rules_dir}/75-probe_mtd.rules
%{udev_rules_dir}/78-sound-card.rules
%{udev_libdir}/cdrom_id
%{udev_libdir}/collect
%{udev_libdir}/mtd_probe
%{udev_libdir}/v4l_id

%files locale -f %{name}.lang
%{_prefix}/lib/%{name}/catalog/*.catalog

%files polkit
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.resolve1.policy
%{_datadir}/polkit-1/rules.d/systemd-networkd.rules

%files zsh-completion
%{_datadir}/zsh/site-functions/*

%files bash-completion
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/*
