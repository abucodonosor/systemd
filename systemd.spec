Summary:	A System and Session Manager
Name:		systemd
Version:	11
Release:	%mkrel 3
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/systemd
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.bz2
Source1:	halt

# (bor) use /cgroup until kernel supports /sys/fs/cgroup
Patch0:		0001-Revert-cgroup-mount-cgroup-file-systems-to-sys-fs-cg.patch
# (bor) needed because patch0 touches man sources
Patch1:		0002-Use-xhtml-not-xhtml-1_1-which-does-not-exist-in-our-.patch
# (bor) export INIT_VERSION to allow use of legacy /sbin/halt from sysvinit
Patch2:		0003-Export-INIT_VERSION-for-shutdown-commands.patch
# (bor) use local version of /etc/init.d/halt that does not unmount cgroup
Patch3:		0004-use-local-version-of-halt-that-does-not-unmount-cgro.patch
# (bor) for now we use messabus service to start D-Bus
Patch4:		0005-Set-special-D-Bus-service-to-messagebus.service.patch
# (bor) adapt vconsole service to Mandriva configuration
Patch5:		0006-Adapt-vconsole-setup-to-Mandriva-configuration-based.patch
# (bor) adapt locale setup to Mandriva configuration
Patch6:		0007-Fully-support-all-i18n-environments-in-Mandriva.patch
# (bor) distinguish between network and $network to break dependency loop
Patch7:		0008-Use-network-for-special-network-service.patch
# (bor) revert to using hardcoded /bin/sh in single user mode
Patch8:		0009-Revert-to-using-bin-sh-for-single-user-shell.patch
# (bor) fix systemctl enable getty@.service (upstream)
Patch9:		0010-systemctl-fix-systemctl-enable-getty-.service.patch

BuildRequires:	dbus-devel >= 1.4.0
BuildRequires:	libudev-devel >= 160
BuildRequires:	libcap-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pam-devel
BuildRequires:	libxslt-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	dbus-glib-devel
BuildRequires:	vala >= 0.9
BuildRequires:	gtk2-devel glib2-devel libnotify-devel
Requires:	systemd-units = %{version}-%{release}
Requires:	dbus >= 1.3.2
Requires:	udev >= 160
Requires:	initscripts
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
systemd is a system and session manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package units
Summary:	Configuration files, directories and installation tool for systemd
Group:		System/Configuration/Boot and Init
Requires:	%{name} = %{version}-%{release}

%description units
Basic configuration files, directories and installation tool for the systemd
system and session manager.

%package gtk
Summary:        Graphical frontend for systemd
Group:          System/Configuration/Boot and Init
Requires:       %{name} = %{version}-%{release}

%description gtk
Graphical front-end for systemd.

%package sysvinit
Summary:        System V init tools
Group:          System/Configuration/Boot and Init
Requires:       %{name} = %{version}-%{release}
#(tpg) do not obsolete sysvinit

%description sysvinit
Drop-in replacement for the System V init tools of systemd.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--with-rootdir= \
	--with-distro=fedora \
	--with-sysvinit-path=%{_initrddir} \
	--with-sysvrcd-path=%{_sysconfdir}/rc.d \
	--with-syslog-service=rsyslog.service

%make

%install
rm -rf %{buildroot}

%makeinstall_std
find %{buildroot} \( -name '*.a' -o -name '*.la' \) -exec rm {} \;

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
mkdir -p %{buildroot}/sbin
ln -s ../bin/systemd %{buildroot}/sbin/init
ln -s ../bin/systemctl %{buildroot}/sbin/reboot
ln -s ../bin/systemctl %{buildroot}/sbin/halt
ln -s ../bin/systemctl %{buildroot}/sbin/poweroff
ln -s ../bin/systemctl %{buildroot}/sbin/shutdown
ln -s ../bin/systemctl %{buildroot}/sbin/telinit
ln -s ../bin/systemctl %{buildroot}/sbin/runlevel

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
rm -r %{buildroot}%{_sysconfdir}/systemd/system/*.target.wants
rm -f %{buildroot}%{_sysconfdir}/systemd/system/display-manager.service

# And the default symlink we generate automatically based on inittab
rm -f %{buildroot}%{_sysconfdir}/systemd/system/default.target

# temporary workaround until initscripts support is avaialble
install -m 0755 %{SOURCE1} %{buildroot}/lib/systemd
ln -s halt %{buildroot}/lib/systemd/reboot

# The following services are currently executed by rc.sysinit
# tmpwatch installs own cron script
pushd %{buildroot}/lib/systemd/system/basic.target.wants && {
	rm -f sysctl.service
	rm -f systemd-modules-load.service
	rm -f systemd-random-seed-load.service
	rm -f systemd-tmpfiles.service
	rm -f tmpwatch.service
	rm -f tmpwatch.timer
popd
}

# The following services are currently executed by rc.sysinit
pushd %{buildroot}/lib/systemd/system/local-fs.target.wants && {
	rm -f remount-rootfs.service
	rm -f systemd-remount-api-vfs.service
	rm -f var-lock.mount
	rm -f var-run.mount
popd
}

# (bor) For now mounts are performed by initscripts (Fedora)
sed -i -e 's/^#MountAuto=yes$/MountAuto=no/' \
        -e 's/^#SwapAuto=yes$/SwapAuto=no/' %{buildroot}/etc/systemd/system.conf

%clean
rm -rf %{buildroot}

%triggerin -- glibc
# reexec daemon on self or glibc update to avoid busy / on shutdown
# trigger is executed on both self and target install so no need to have
# extra own post
if [ $1 -ge 2 -o $2 -ge 2 ] ; then
	/bin/systemctl daemon-reexec 2>&1 || :
fi

%post units
if [ $1 -eq 1 ] ; then
        # Try to read default runlevel from the old inittab if it exists
        runlevel=$(/bin/awk -F ':' '$3 == "initdefault" && $1 !~ "^#" { print $2 }' /etc/inittab 2> /dev/null)
        if [ -z "$runlevel" ] ; then
                target="/lib/systemd/system/graphical.target"
        else
                target="/lib/systemd/system/runlevel$runlevel.target"
        fi

        # And symlink what we found to the new-style default.target
        /bin/ln -sf "$target" %{_sysconfdir}/systemd/system/default.target 2>&1 || :

        # Enable the services we install by default.
	# (bor) do not enable prefdm.service, we start it in initscript
        /bin/systemctl enable \
                getty@.service \
                rc-local.service \
                remote-fs.target 2>&1 || :
fi

%preun units
if [ $1 -eq 0 ] ; then
        /bin/systemctl disable \
                getty@.service \
                rc-local.service \
                remote-fs.target 2>&1 || :

        /bin/rm -f /etc/systemd/system/default.target 2>&1 || :
fi

%postun units
if [ $1 -ge 1 ] ; then
        /bin/systemctl daemon-reload 2>&1 || :
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_sysconfdir}/rc.d/init.d/reboot
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%dir %{_sysconfdir}/systemd/session
%{_sysconfdir}/xdg/systemd
/bin/systemd
/bin/systemd-ask-password
/bin/systemd-notify
%dir /lib/systemd
/lib/systemd/systemd-*
# FIXME to be removed later
/lib/systemd/halt
/lib/systemd/reboot
/lib/udev/rules.d/*.rules
/%{_lib}/security/pam_systemd.so
%{_bindir}/systemd-cgls
%{_mandir}/man1/systemd.*
%{_mandir}/man1/systemd-notify.*
%{_mandir}/man1/systemd-cgls.*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/pam_systemd.*
%{_datadir}/systemd
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.*.xml
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_docdir}/systemd

# Joint ownership with libcgroup
%dir /cgroup

%files units
%defattr(-,root,root)
/bin/systemctl
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/tmpfiles.d
%config(noreplace) %{_sysconfdir}/tmpfiles.d/*.conf
/lib/systemd/system
%{_mandir}/man1/systemctl.*
%{_datadir}/pkgconfig/systemd.pc

%files gtk
%defattr(-,root,root)
%{_bindir}/systemadm
%{_bindir}/systemd-ask-password-agent
%{_mandir}/man1/systemadm.*

%files sysvinit
%defattr(-,root,root,-)
/sbin/init
/sbin/reboot
/sbin/halt
/sbin/poweroff
/sbin/shutdown
/sbin/telinit
/sbin/runlevel
%{_mandir}/man1/init.*
%{_mandir}/man8/halt.*
%{_mandir}/man8/reboot.*
%{_mandir}/man8/shutdown.*
%{_mandir}/man8/poweroff.*
%{_mandir}/man8/telinit.*
%{_mandir}/man8/runlevel.*
