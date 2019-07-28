%global libauditver     2.1.3-4
%global libsepolver     2.9-1
%global libsemanagever  2.9-1
%global libselinuxver   2.9-1
%global sepolgenver     2.9

%global generatorsdir %{_prefix}/lib/systemd/system-generators

# Disable automatic compilation of Python files in extra directories
%global _python_bytecompile_extra 0

Summary: SELinux policy core utilities
Name:    policycoreutils
Version: 2.9
Release: 1
License: GPLv2
# https://github.com/SELinuxProject/selinux/wiki/Releases
Source0: https://github.com/SELinuxProject/selinux/releases/download/20190315/policycoreutils-2.9.tar.gz
Source1: https://github.com/SELinuxProject/selinux/releases/download/20190315/selinux-python-2.9.tar.gz
Source2: https://github.com/SELinuxProject/selinux/releases/download/20190315/selinux-gui-2.9.tar.gz
Source3: https://github.com/SELinuxProject/selinux/releases/download/20190315/selinux-sandbox-2.9.tar.gz
Source4: https://github.com/SELinuxProject/selinux/releases/download/20190315/selinux-dbus-2.9.tar.gz
Source5: https://github.com/SELinuxProject/selinux/releases/download/20190315/semodule-utils-2.9.tar.gz
Source6: https://github.com/SELinuxProject/selinux/releases/download/20190315/restorecond-2.9.tar.gz
URL:     https://github.com/SELinuxProject/selinux
Source13: system-config-selinux.png
Source14: sepolicy-icons.tgz
Source15: selinux-autorelabel
Source16: selinux-autorelabel.service
Source17: selinux-autorelabel-mark.service
Source18: selinux-autorelabel.target
Source19: selinux-autorelabel-generator.sh
Source20: policycoreutils-po.tgz
Source21: python-po.tgz
Source22: gui-po.tgz
Source23: sandbox-po.tgz
# download https://raw.githubusercontent.com/fedora-selinux/scripts/master/selinux/make-fedora-selinux-patch.sh
# run:
# HEAD https://github.com/fedora-selinux/selinux/commit/431f72836d6c02450725cf6ffb1c7223b9fa6acc
# $ for i in policycoreutils selinux-python selinux-gui selinux-sandbox selinux-dbus semodule-utils restorecond; do
#   VERSION=2.9 ./make-fedora-selinux-patch.sh $i
# done
Patch0:  policycoreutils-fedora.patch
Patch1:  selinux-python-fedora.patch
Patch2:  selinux-gui-fedora.patch
Patch3:  selinux-sandbox-fedora.patch
# Patch4:  selinux-dbus-fedora.patch
Patch5:  semodule-utils-fedora.patch
# Patch6:  restorecond-fedora.patch
Obsoletes: policycoreutils < 2.0.61-2
Conflicts: filesystem < 3, selinux-policy-base < 3.13.1-138
# initscripts < 9.66 shipped fedora-autorelabel services which are renamed to selinux-relabel
Conflicts: initscripts < 9.66
Provides: /sbin/fixfiles
Provides: /sbin/restorecon


BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(dbus-1) 
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	sepol-static-devel >= %{libsepolver} 
BuildRequires:	semanage-static-devel >= %{libsemanagever} 
BuildRequires:	pkgconfig(libselinux) >= %{libselinuxver}  
BuildRequires:	pkgconfig(libcap) 
BuildRequires:	python2-devel python3-devel
BuildRequires:	systemd
BuildRequires:	pam-devel
BuildRequires:	audit-devel
Requires:	util-linux grep gawk diffutils rpm sed coreutils
Requires:	libsepol >= %{libsepolver} coreutils libselinux-utils >= %{libselinuxver}

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

policycoreutils contains the policy core utilities that are required
for basic operation of a SELinux system.  These utilities include
load_policy to load policies, setfiles to label filesystems, newrole
to switch roles.

%prep
# create selinux/ directory and extract sources
%setup -q -c -n selinux
%setup -q -T -D -a 1 -n selinux
%setup -q -T -D -a 2 -n selinux
%setup -q -T -D -a 3 -n selinux
%setup -q -T -D -a 4 -n selinux
%setup -q -T -D -a 5 -n selinux
%setup -q -T -D -a 6 -n selinux
%patch0 -p0 -b .policycoreutils-fedora

cp %{SOURCE13} selinux-gui-%{version}/
tar -xvf %{SOURCE14} -C selinux-python-%{version}/sepolicy/
%patch1 -p0 -b .selinux-python
%patch2 -p0 -b .selinux-gui
%patch3 -p0 -b .selinux-sandbox
# %patch4 -p0 -b .selinux-dbus
%patch5 -p0 -b .semodule-utils
# %patch6 -p0 -b .restorecond

# Since patches containing translation changes were too big, translations were moved to separate tarballs
# For more information see README.translations
tar -x -f %{SOURCE20} -C policycoreutils-%{version} -z
tar -x -f %{SOURCE21} -C selinux-python-%{version} -z
tar -x -f %{SOURCE22} -C selinux-gui-%{version} -z
tar -x -f %{SOURCE23} -C selinux-sandbox-%{version} -z

%build
%serverbuild_hardened
export PYTHON=%{__python3}

make CC=%{__cc} -C policycoreutils-%{version} LSPP_PRIV=y SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a" all
make CC=%{__cc} -C selinux-python-%{version} SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make CC=%{__cc} -C selinux-gui-%{version} SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make CC=%{__cc} -C selinux-sandbox-%{version} SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make CC=%{__cc} -C selinux-dbus-%{version} SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make CC=%{__cc} -C semodule-utils-%{version} SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make CC=%{__cc} -C restorecond-%{version} SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man8
%{__mkdir} -p %{buildroot}/%{_usr}/share/doc/%{name}/

make CC=%{__cc} -C policycoreutils-%{version} LSPP_PRIV=y  DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a" install
make CC=%{__cc} -C selinux-python-%{version} PYTHON=%{__python2} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make CC=%{__cc} -C selinux-python-%{version} PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make CC=%{__cc} -C selinux-gui-%{version} PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make CC=%{__cc} -C selinux-sandbox-%{version} PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make CC=%{__cc} -C selinux-dbus-%{version} PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make CC=%{__cc} -C semodule-utils-%{version} PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make CC=%{__cc} -C restorecond-%{version} PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" SYSTEMDDIR="/lib/systemd" install


# Systemd
rm -rf %{buildroot}/%{_sysconfdir}/rc.d/init.d/restorecond
rm -f %{buildroot}/usr/share/man/ru/man8/genhomedircon.8.*
rm -f %{buildroot}/usr/share/man/ru/man8/open_init_pty.8.*
rm -f %{buildroot}/usr/share/man/ru/man8/semodule_deps.8.*
rm -f %{buildroot}/usr/share/man/man8/open_init_pty.8*
rm -f %{buildroot}/usr/sbin/open_init_pty
rm -f %{buildroot}/usr/sbin/run_init
rm -f %{buildroot}/usr/share/man/ru/man8/run_init.8*
rm -f %{buildroot}/usr/share/man/man8/run_init.8*
rm -f %{buildroot}/etc/pam.d/run_init*

# https://bugzilla.redhat.com/show_bug.cgi?id=1566618
# we don't need python2 sepolicy gui files anymore
rm -f %{buildroot}%{python2_sitelib}/sepolicy/gui.*
rm -f %{buildroot}%{python2_sitelib}/sepolicy/sepolicy.glade
rm -rf %{buildroot}%{python2_sitelib}/sepolicy/help

mkdir -m 755 -p %{buildroot}/%{generatorsdir}
mkdir -p %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE16} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE17} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE18} %{buildroot}/%{_unitdir}/
install -m 755 -p %{SOURCE19} %{buildroot}/%{generatorsdir}/
install -m 755 -p %{SOURCE15} %{buildroot}/%{_libexecdir}/selinux/

# clean up ~ files from pathfix - https://bugzilla.redhat.com/show_bug.cgi?id=1546990
find %{buildroot}%{python2_sitelib} %{buildroot}%{python2_sitearch} \
     %{buildroot}%{python3_sitelib} %{buildroot}%{python3_sitearch} \
     %{buildroot}%{_sbindir} %{buildroot}%{_bindir} %{buildroot}%{_datadir} \
     -type f -name '*~' | xargs rm -f

# Manually invoke the python byte compile macro for each path that needs byte
# compilation.
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/system-config-selinux

%find_lang policycoreutils
%find_lang selinux-python
%find_lang selinux-gui
%find_lang selinux-sandbox

%package python-utils
Summary:    SELinux policy core python utilities
Requires:   python3-policycoreutils = %{version}-%{release}
Obsoletes:  policycoreutils-python <= 2.4-4
BuildArch:  noarch

%description python-utils
The policycoreutils-python-utils package contains the management tools use to manage
an SELinux environment.

%files python-utils
%{_sbindir}/semanage
%{_bindir}/chcat
%{_bindir}/sandbox
%{_bindir}/audit2allow
%{_bindir}/audit2why
%{_mandir}/man1/audit2allow.1*
%{_mandir}/ru/man1/audit2allow.1*
%{_mandir}/man1/audit2why.1*
%{_sysconfdir}/dbus-1/system.d/org.selinux.conf
%{_mandir}/man8/chcat.8*
%{_mandir}/ru/man8/chcat.8*
%{_mandir}/man8/sandbox.8*
%{_mandir}/man8/semanage*.8*
%{_mandir}/ru/man8/semanage.8*
%{_datadir}/bash-completion/completions/semanage

%package dbus
Summary:    SELinux policy core DBUS api
Requires:   python3-policycoreutils = %{version}-%{release}
Requires:   python3-slip-dbus
BuildArch:  noarch

%description dbus
The policycoreutils-dbus package contains the management DBUS API use to manage
an SELinux environment.

%files dbus
%{_sysconfdir}/dbus-1/system.d/org.selinux.conf
%{_datadir}/dbus-1/system-services/org.selinux.service
%{_datadir}/polkit-1/actions/org.selinux.policy
%{_datadir}/polkit-1/actions/org.selinux.config.policy
%{_datadir}/system-config-selinux/selinux_server.py
%dir %{_datadir}/system-config-selinux/__pycache__
%{_datadir}/system-config-selinux/__pycache__/selinux_server.*

%package -n python3-policycoreutils
%{?python_provide:%python_provide python3-policycoreutils}
# Remove before F31
Provides: %{name}-python3 = %{version}-%{release}
Provides: %{name}-python3 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}
Summary: SELinux policy core python3 interfaces
Requires:policycoreutils = %{version}-%{release}
Requires:python-libsemanage >= %{libsemanagever} python-selinux
# no python3-audit-libs yet
Requires: python-audit >=  %{libauditver}
Requires: checkpolicy
Requires: python-setools >= 4.1.1
BuildArch: noarch

%description -n python3-policycoreutils
The python3-policycoreutils package contains the interfaces that can be used
by python 3 in an SELinux environment.

%files -f selinux-python.lang -n python3-policycoreutils
%{python3_sitelib}/seobject.py*
%{python3_sitelib}/__pycache__
%{python3_sitelib}/sepolgen
%dir %{python3_sitelib}/sepolicy
%{python3_sitelib}/sepolicy/templates
%dir %{python3_sitelib}/sepolicy/help
%{python3_sitelib}/sepolicy/help/*
%{python3_sitelib}/sepolicy/__init__.py*
%{python3_sitelib}/sepolicy/booleans.py*
%{python3_sitelib}/sepolicy/communicate.py*
%{python3_sitelib}/sepolicy/generate.py*
%{python3_sitelib}/sepolicy/interface.py*
%{python3_sitelib}/sepolicy/manpage.py*
%{python3_sitelib}/sepolicy/network.py*
%{python3_sitelib}/sepolicy/transition.py*
%{python3_sitelib}/sepolicy/sedbus.py*
%{python3_sitelib}/sepolicy*.egg-info
%{python3_sitelib}/sepolicy/__pycache__

%package -n python2-policycoreutils
%{?python_provide:%python_provide python2-policycoreutils}
# Remove before F30
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Summary: SELinux policy core python2 utilities
Requires:policycoreutils = %{version}-%{release}
Requires:python2-libsemanage >= %{libsemanagever} python2-libselinux
# no python2-audit-libs yet
Requires: python2-audit >=  %{libauditver}
Obsoletes: policycoreutils < 2.0.61-2
Requires: python2-IPy
Requires: checkpolicy
Requires: python2-setools >= 4.1.1
Requires: python2-ipaddress
BuildArch: noarch

%description -n python2-policycoreutils
The policycoreutils-python package contains the management tools use to manage
an SELinux environment.

%files -n python2-policycoreutils
%{python2_sitelib}/seobject.py*
%{python2_sitelib}/sepolgen
%dir %{python2_sitelib}/sepolicy
%{python2_sitelib}/sepolicy/templates
%{python2_sitelib}/sepolicy/__init__.py*
%{python2_sitelib}/sepolicy/booleans.py*
%{python2_sitelib}/sepolicy/communicate.py*
%{python2_sitelib}/sepolicy/generate.py*
%{python2_sitelib}/sepolicy/interface.py*
%{python2_sitelib}/sepolicy/manpage.py*
%{python2_sitelib}/sepolicy/network.py*
%{python2_sitelib}/sepolicy/transition.py*
%{python2_sitelib}/sepolicy/sedbus.py*
%{python2_sitelib}/sepolicy*.egg-info

%package devel
Summary: SELinux policy core policy devel utilities
Requires: policycoreutils-python-utils = %{version}-%{release}
Requires: /usr/bin/make
Requires: selinux-policy-devel

%description devel
The policycoreutils-devel package contains the management tools use to develop policy in an SELinux environment.

%files devel
%{_bindir}/sepolgen
%{_bindir}/sepolgen-ifgen
%{_bindir}/sepolgen-ifgen-attr-helper
%dir  /var/lib/sepolgen
/var/lib/sepolgen/perm_map
%{_bindir}/sepolicy
%{_mandir}/man8/sepolgen.8*
%{_mandir}/man8/sepolicy-booleans.8*
%{_mandir}/man8/sepolicy-generate.8*
%{_mandir}/man8/sepolicy-interface.8*
%{_mandir}/man8/sepolicy-network.8*
%{_mandir}/man8/sepolicy.8*
%{_mandir}/man8/sepolicy-communicate.8*
%{_mandir}/man8/sepolicy-manpage.8*
%{_mandir}/man8/sepolicy-transition.8*
%{_usr}/share/bash-completion/completions/sepolicy

%package sandbox
Summary: SELinux sandbox utilities
Requires: python3-policycoreutils = %{version}-%{release}
Requires: x11-server-xephyr /usr/bin/rsync /usr/bin/xmodmap
BuildRequires: libcap-ng-devel

%description sandbox
The policycoreutils-sandbox package contains the scripts to create graphical
sandboxes

%files -f selinux-sandbox.lang sandbox
%config(noreplace) %{_sysconfdir}/sysconfig/sandbox
%{_datadir}/sandbox/sandboxX.sh
%{_datadir}/sandbox/start
%caps(cap_setpcap,cap_setuid,cap_fowner,cap_dac_override,cap_sys_admin,cap_sys_nice=pe) %{_sbindir}/seunshare
%{_mandir}/man8/seunshare.8*
%{_mandir}/man5/sandbox.5*

%package newrole
Summary: The newrole application for RBAC/MLS
Requires: policycoreutils = %{version}-%{release}

%description newrole
RBAC/MLS policy machines require newrole as a way of changing the role
or level of a logged in user.

%files newrole
%attr(0755,root,root) %caps(cap_dac_read_search,cap_setpcap,cap_audit_write,cap_sys_admin,cap_fowner,cap_chown,cap_dac_override=pe) %{_bindir}/newrole
%{_mandir}/man1/newrole.1.*
%config(noreplace) %{_sysconfdir}/pam.d/newrole

%package gui
Summary: SELinux configuration GUI
Requires: policycoreutils-devel = %{version}-%{release}, python3-policycoreutils = %{version}-%{release}
Requires: policycoreutils-dbus = %{version}-%{release}
BuildRequires: desktop-file-utils
BuildArch: noarch

%description gui
system-config-selinux is a utility for managing the SELinux environment

%files -f selinux-gui.lang gui
%{_bindir}/system-config-selinux
%{_bindir}/selinux-polgengui
%{_datadir}/applications/sepolicy.desktop
%{_datadir}/applications/system-config-selinux.desktop
%{_datadir}/applications/selinux-polgengui.desktop
%{_datadir}/icons/hicolor/24x24/apps/system-config-selinux.png
%{_datadir}/pixmaps/system-config-selinux.png
%dir %{_datadir}/system-config-selinux
%dir %{_datadir}/system-config-selinux/__pycache__
%{_datadir}/system-config-selinux/system-config-selinux.png
%{_datadir}/system-config-selinux/*Page.py
%{_datadir}/system-config-selinux/__pycache__/*Page.*
%{_datadir}/system-config-selinux/system-config-selinux.py
%{_datadir}/system-config-selinux/__pycache__/system-config-selinux.*
%{_datadir}/system-config-selinux/*.ui
%{python3_sitelib}/sepolicy/gui.py*
%{python3_sitelib}/sepolicy/sepolicy.glade
%{_datadir}/icons/hicolor/*/apps/sepolicy.png
%{_datadir}/pixmaps/sepolicy.png
%{_mandir}/man8/system-config-selinux.8*
%{_mandir}/man8/selinux-polgengui.8*
%{_mandir}/man8/sepolicy-gui.8*

%files -f %{name}.lang
%{_sbindir}/restorecon
%{_sbindir}/restorecon_xattr
%{_sbindir}/fixfiles
%{_sbindir}/setfiles
%{_sbindir}/load_policy
%{_sbindir}/genhomedircon
%{_sbindir}/setsebool
%{_sbindir}/semodule
%{_sbindir}/sestatus
%{_bindir}/secon
%{_bindir}/semodule_expand
%{_bindir}/semodule_link
%{_bindir}/semodule_package
%{_bindir}/semodule_unpackage
%{_libexecdir}/selinux/hll
%{_libexecdir}/selinux/selinux-autorelabel
%{_unitdir}/selinux-autorelabel-mark.service
%{_unitdir}/selinux-autorelabel.service
%{_unitdir}/selinux-autorelabel.target
%{generatorsdir}/selinux-autorelabel-generator.sh
%config(noreplace) %{_sysconfdir}/sestatus.conf
%{_mandir}/man5/selinux_config.5.*
%{_mandir}/man5/sestatus.conf.5.*
%{_mandir}/man8/fixfiles.8*
%{_mandir}/ru/man8/fixfiles.8*
%{_mandir}/man8/load_policy.8*
%{_mandir}/ru/man8/load_policy.8*
%{_mandir}/man8/restorecon.8*
%{_mandir}/ru/man8/restorecon.8*
%{_mandir}/man8/restorecon_xattr.8*
%{_mandir}/man8/semodule.8*
%{_mandir}/ru/man8/semodule.8*
%{_mandir}/man8/sestatus.8*
%{_mandir}/ru/man8/sestatus.8*
%{_mandir}/man8/setfiles.8*
%{_mandir}/ru/man8/setfiles.8*
%{_mandir}/man8/setsebool.8*
%{_mandir}/ru/man8/setsebool.8*
%{_mandir}/man1/secon.1*
%{_mandir}/ru/man1/secon.1*
%{_mandir}/man8/genhomedircon.8*
%{_mandir}/man8/semodule_expand.8*
%{_mandir}/ru/man8/semodule_expand.8*
%{_mandir}/man8/semodule_link.8*
%{_mandir}/ru/man8/semodule_link.8*
%{_mandir}/man8/semodule_unpackage.8*
%{_mandir}/man8/semodule_package.8*
%{_mandir}/ru/man8/semodule_package.8*
%dir %{_datadir}/bash-completion
%{_datadir}/bash-completion/completions/setsebool
%{!?_licensedir:%global license %%doc}
%license policycoreutils-%{version}/COPYING
%doc %{_usr}/share/doc/%{name}

%package restorecond
Summary: SELinux restorecond utilities
BuildRequires: systemd-units

%description restorecond
The policycoreutils-restorecond package contains the restorecond service.

%files restorecond
%{_sbindir}/restorecond
%{_unitdir}/restorecond.service
%config(noreplace) %{_sysconfdir}/selinux/restorecond.conf
%config(noreplace) %{_sysconfdir}/selinux/restorecond_user.conf
%{_sysconfdir}/xdg/autostart/restorecond.desktop
%{_datadir}/dbus-1/services/org.selinux.Restorecond.service
%{_mandir}/man8/restorecond.8*
%{_mandir}/ru/man8/restorecond.8*
/usr/share/man/ru/man1/audit2why.1.*
/usr/share/man/ru/man1/newrole.1.*
/usr/share/man/ru/man5/sandbox.5.*
/usr/share/man/ru/man5/selinux_config.5.*
/usr/share/man/ru/man5/sestatus.conf.5.*
/usr/share/man/ru/man8/genhomedircon.8.*
/usr/share/man/ru/man8/open_init_pty.8.*
/usr/share/man/ru/man8/restorecon_xattr.8.*
/usr/share/man/ru/man8/sandbox.8.*
/usr/share/man/ru/man8/selinux-polgengui.8.*
/usr/share/man/ru/man8/semanage-boolean.8.*
/usr/share/man/ru/man8/semanage-dontaudit.8.*
/usr/share/man/ru/man8/semanage-export.8.*
/usr/share/man/ru/man8/semanage-fcontext.8.*
/usr/share/man/ru/man8/semanage-ibendport.8.*
/usr/share/man/ru/man8/semanage-ibpkey.8.*
/usr/share/man/ru/man8/semanage-import.8.*
/usr/share/man/ru/man8/semanage-interface.8.*
/usr/share/man/ru/man8/semanage-login.8.*
/usr/share/man/ru/man8/semanage-module.8.*
/usr/share/man/ru/man8/semanage-node.8.*
/usr/share/man/ru/man8/semanage-permissive.8.*
/usr/share/man/ru/man8/semanage-port.8.*
/usr/share/man/ru/man8/semanage-user.8.*
/usr/share/man/ru/man8/semodule_unpackage.8.*
/usr/share/man/ru/man8/sepolgen.8.*
/usr/share/man/ru/man8/sepolicy-booleans.8.*
/usr/share/man/ru/man8/sepolicy-communicate.8.*
/usr/share/man/ru/man8/sepolicy-generate.8.*
/usr/share/man/ru/man8/sepolicy-gui.8.*
/usr/share/man/ru/man8/sepolicy-interface.8.*
/usr/share/man/ru/man8/sepolicy-manpage.8.*
/usr/share/man/ru/man8/sepolicy-network.8.*
/usr/share/man/ru/man8/sepolicy-transition.8.*
/usr/share/man/ru/man8/sepolicy.8.*
/usr/share/man/ru/man8/seunshare.8.*
/usr/share/man/ru/man8/system-config-selinux.8.*

%{!?_licensedir:%global license %%doc}
%license policycoreutils-%{version}/COPYING

%post
%systemd_post selinux-autorelabel-mark.service

%preun
%systemd_preun selinux-autorelabel-mark.service

%post restorecond
%systemd_post restorecond.service

%preun restorecond
%systemd_preun restorecond.service

%postun restorecond
%systemd_postun_with_restart restorecond.service
