# macros for sysvinit transition - should be equal to
# sysvinit %version-%release-plus-1
%define sysvinit_version 2.87
%define sysvinit_release %mkrel 12

# (eugeni) for backports and old distributions, rely on EVRD as well
%if %mdkversion < 201100
%define EVRD %{?epoch:%{epoch}:}%{?version:%{version}}%{?release:-%{release}}%{?distepoch::%{distepoch}}
%endif


Summary:	A System and Session Manager
Name:		systemd
Version:	29
Release:	%mkrel 3
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/systemd
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.bz2

# (bor) clean up directories on boot as done by rc.sysinit
Patch16:	systemd-18-clean-dirs-on-boot.patch
# (bor) reset /etc/mtab on boot (why is it not a link)?
Patch17:	systemd-18-reset-mtab-on-boot.patch
# (bor) allow explicit stdout configuration for SysV scripts
#Patch18:	systemd-19-sysv_std_output.patch
# (bor) fix potential deadlock when onseshot unit is not finished
Patch19:	systemd-19-apply-timeoutsec-to-oneshot-too.patch
# (bor) network filesystems do not need quota service (mdv#62746)
#Patch21:	systemd-19-no-quotacheck-for-netfs.patch

BuildRequires:	cryptsetup-devel
BuildRequires:	dbus-devel >= 1.4.0
BuildRequires:	libudev-devel >= 160
BuildRequires:	libcap-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pam-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	vala >= 0.9
BuildRequires:	gtk2-devel glib2-devel libnotify-devel
BuildRequires:  libxslt-devel
BuildRequires:  docbook-style-xsl
# TODO for P12, remove when it is removed
BuildRequires:	automake autoconf
Requires:	systemd-units = %{EVRD}
Requires:	dbus >= 1.3.2
Requires:	udev >= 160
Requires:	initscripts >= 9.21-3mdv2011.0
Requires:	util-linux-ng >= 2.18-2mdv2011.0
Conflicts:	initscripts < 9.24
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
# (eugeni) systemd should work as a drop-in replacement for sysvinit, but not obsolete it
Provides:       sysvinit = %sysvinit_version-%sysvinit_release, SysVinit = %sysvinit_release-%sysvinit_release
Conflicts:      sysvinit < %sysvinit_version-%sysvinit_release, SysVinit < %sysvinit_release-%sysvinit_release

%description sysvinit
Drop-in replacement for the System V init tools of systemd.

%prep
%setup -q
%apply_patches
find src/ -name "*.vala" -exec touch '{}' \;

%build
# TODO for P12, remove when it is removed
autoreconf -fis
%configure2_5x \
	--with-rootdir=

%make

%install
rm -rf %{buildroot}

%makeinstall_std
find %{buildroot} \( -name '*.a' -o -name '*.la' \) -exec rm {} \;

# (bor) create late shutdown directory
mkdir -p %{buildroot}/lib/systemd/system-shutdown

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

# We are not prepared to deal with tmpfs /var/run or /var/lock
pushd %{buildroot}/lib/systemd/system/local-fs.target.wants && {
        rm -f var-lock.mount
        rm -f var-run.mount
popd
}

# (bor) make sure we own directory for bluez to install service
mkdir -p %{buildroot}/lib/systemd/system/bluetooth.target.wants

# use consistent naming and permissions for completion scriplets
mv %{buildroot}%{_sysconfdir}/bash_completion.d/systemctl-bash-completion.sh \
    %{buildroot}%{_sysconfdir}/bash_completion.d/systemctl
chmod 644 %{buildroot}%{_sysconfdir}/bash_completion.d/systemctl

# (bor) disable legacy output to console, it just messes things up
sed -i -e 's/^#SysVConsole=yes$/SysVConsole=no/' \
	%{buildroot}/etc/systemd/system.conf

# (bor) enable rpcbind.target by default so we have something to plug
#	portmapper service into
ln -s ../rpcbind.target %{buildroot}/lib/systemd/system/multi-user.target.wants

# (bor) machine-id-setup is in /sbin in post-v20
install -d %{buildroot}/sbin && \
	mv %{buildroot}/bin/systemd-machine-id-setup %{buildroot}/sbin

# (eugeni) install /run
mkdir %{buildroot}/run

# add missing ttys (mdv #63600)
mkdir -p %{buildroot}/etc/systemd/system/getty.target.wants
pushd %{buildroot}/etc/systemd/system/getty.target.wants
	for _term in 1 2 3 4 5 6 ; do
	ln -s /lib/systemd/system/getty@.service getty@tty$_term.service
	done
popd

%clean
rm -rf %{buildroot}

%triggerin -- glibc
# reexec daemon on self or glibc update to avoid busy / on shutdown
# trigger is executed on both self and target install so no need to have
# extra own post
if [ $1 -ge 2 -o $2 -ge 2 ] ; then
	/bin/systemctl daemon-reexec 2>&1 || :
fi

%post
/sbin/systemd-machine-id-setup

%triggerin units -- %{name}-units < 19-4
# Enable the services we install by default.
/bin/systemctl --quiet enable \
	hwclock-load.service \
	quotaon.service \
	quotacheck.service \
	systemd-readahead-replay.service \
	systemd-readahead-collect.service \
	2>&1 || :
# rc-local is now enabled by default in base package
rm -f /etc/systemd/system/multi-user.target.wants/rc-local.service || :

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
	/bin/systemctl --quiet enable \
		hwclock-load.service \
		getty@.service \
		quotaon.service \
		quotacheck.service \
		remote-fs.target \
		systemd-readahead-replay.service \
		systemd-readahead-collect.service \
		2>&1 || :
fi

%preun units
if [ $1 -eq 0 ] ; then
        /bin/systemctl --quiet disable \
		hwclock-load.service \
		getty@.service \
		quotaon.service \
		quotacheck.service \
		remote-fs.target \
		systemd-readahead-replay.service \
		systemd-readahead-collect.service \
		2>&1 || :

        /bin/rm -f /etc/systemd/system/default.target 2>&1 || :
fi

%postun units
if [ $1 -ge 1 ] ; then
        /bin/systemctl daemon-reload 2>&1 || :
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%dir %{_sysconfdir}/tmpfiles.d
%{_sysconfdir}/xdg/systemd
/bin/systemd
/bin/systemd-ask-password
/bin/systemd-notify
/bin/systemd-tmpfiles
/bin/systemd-tty-ask-password-agent
/sbin/systemd-machine-id-setup
%dir /lib/systemd
%dir /lib/systemd/system-generators
%dir /lib/systemd/system-shutdown
/lib/systemd/systemd-*
/lib/systemd/system-generators/*
/lib/udev/rules.d/*.rules
%dir /usr/lib/tmpfiles.d/
/usr/lib/tmpfiles.d/legacy.conf
/usr/lib/tmpfiles.d/systemd.conf
/usr/lib/tmpfiles.d/x11.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
/%{_lib}/security/pam_systemd.so
%{_bindir}/systemd-analyze
%{_bindir}/systemd-cgls
%{_bindir}/systemd-nspawn
%{_bindir}/systemd-stdio-bridge
%{_mandir}/man1/systemd.*
%{_mandir}/man1/systemd-ask-password.*
%{_mandir}/man1/systemd-notify.*
%{_mandir}/man1/systemd-nspawn.*
%{_mandir}/man1/systemd-cgls.*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/pam_systemd.*
%{_mandir}/man8/systemd-tmpfiles.*
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.*.xml
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_docdir}/systemd

%files units
%defattr(-,root,root)
/bin/systemctl
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%{_sysconfdir}/systemd/system/getty.target.wants/getty@*.service
%{_sysconfdir}/systemd/system/getty.target.wants
%{_sysconfdir}/bash_completion.d/systemctl
/lib/systemd/system
/usr/lib/systemd/
%{_mandir}/man1/systemctl.*
%{_datadir}/pkgconfig/systemd.pc

%files gtk
%defattr(-,root,root)
%{_bindir}/systemadm
%{_bindir}/systemd-gnome-ask-password-agent
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
%dir /run
