%global libauditver     2.1.3-4
%global libsepolver     %{version}-1
%global libsemanagever  %{version}-1
%global libselinuxver   %{version}-1
%global sepolgenver     %{version}

%global generatorsdir %{_prefix}/lib/systemd/system-generators

# Work around build system deficiencies
%undefine _debugsource_packages

# Disable automatic compilation of Python files in extra directories
%global _python_bytecompile_extra 0

Summary: SELinux policy core utilities
Name:    policycoreutils
Version: 3.5
Release: 2
License: GPLv2
# https://github.com/SELinuxProject/selinux/wiki/Releases
Source0: https://github.com/SELinuxProject/selinux/releases/download/%{version}/selinux-%{version}.tar.gz
URL:     https://github.com/SELinuxProject/selinux
Source13: system-config-selinux.png
Source14: sepolicy-icons.tgz
Source15: selinux-autorelabel
Source16: selinux-autorelabel.service
Source17: selinux-autorelabel-mark.service
Source18: selinux-autorelabel.target
Source19: selinux-autorelabel-generator.sh

Patch0001: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0001-sandbox-add-reset-to-Xephyr-as-it-works-better-with-.patch
Patch0002: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0002-Don-t-be-verbose-if-you-are-not-on-a-tty.patch
Patch0003: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0003-sepolicy-generate-Handle-more-reserved-port-types.patch
Patch0004: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0004-sandbox-Use-matchbox-window-manager-instead-of-openb.patch
Patch0005: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0005-Use-SHA-2-instead-of-SHA-1.patch
Patch0006: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0006-python-chcat-Improve-man-pages.patch
Patch0007: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0007-python-audit2allow-Add-missing-options-to-man-page.patch
Patch0008: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0008-python-semanage-Improve-man-pages.patch
Patch0009: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0009-python-audit2allow-Remove-unused-debug-option.patch
Patch0010: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0010-policycoreutils-Add-examples-to-man-pages.patch
Patch0011: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0011-python-sepolicy-Improve-man-pages.patch
Patch0012: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0012-sandbox-Add-examples-to-man-pages.patch
Patch0013: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0013-python-sepolicy-Fix-template-for-confined-user-polic.patch
Patch0014: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0014-python-sepolicy-Fix-spec-file-dependencies.patch
Patch0015: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0015-python-improve-format-strings-for-proper-localizatio.patch
Patch0016: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0016-python-Drop-hard-formating-from-localized-strings.patch
Patch0017: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0017-semanage-Drop-unnecessary-import-from-seobject.patch
Patch0018: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0018-python-update-python.pot.patch
Patch0019: https://src.fedoraproject.org/rpms/policycoreutils/raw/rawhide/f/0019-sepolicy-port-to-dnf4-python-API.patch
Conflicts: filesystem < 3, selinux-policy-base < 3.13.1-138
# initscripts < 9.66 shipped fedora-autorelabel services which are renamed to selinux-relabel
Provides: /sbin/fixfiles
Provides: /sbin/restorecon


BuildRequires:	make
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(dbus-1) 
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	sepol-static-devel >= %{libsepolver} 
BuildRequires:	semanage-static-devel >= %{libsemanagever} 
BuildRequires:	pkgconfig(libselinux) >= %{libselinuxver}  
BuildRequires:	pkgconfig(libcap) 
BuildRequires:	pkgconfig(systemd)
BuildRequires:	python-devel
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
%autosetup -n selinux-%{version} -p 1
cp %{SOURCE13} gui/
tar -xvf %{SOURCE14} -C python/sepolicy/

%build
%serverbuild_hardened
export PYTHON=%{__python}
make -C policycoreutils SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C python SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C gui SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C sandbox SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C dbus SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C semodule-utils SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C restorecond SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man8
%{__mkdir} -p %{buildroot}/%{_usr}/share/doc/%{name}/
 
%make_install -C policycoreutils LSPP_PRIV=y SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a"
 
%make_install -C python PYTHON=%{__python} SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a"
 
%make_install -C gui PYTHON=%{__python} SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a"
 
%make_install -C sandbox PYTHON=%{__python} SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a"
 
%make_install -C dbus PYTHON=%{__python} SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a"
 
%make_install -C semodule-utils PYTHON=%{__python} SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a"
 
%make_install -C restorecond PYTHON=%{__python} SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a"

# Fix perms on newrole so that objcopy can process it
chmod 0755 %{buildroot}%{_bindir}/newrole
 
# Systemd
rm -rf %{buildroot}/%{_sysconfdir}/rc.d/init.d/restorecond
 
rm -f %{buildroot}%{_mandir}/ru/man8/genhomedircon.8*
rm -f %{buildroot}%{_mandir}/ru/man8/open_init_pty.8*
rm -f %{buildroot}%{_mandir}/ru/man8/semodule_deps.8*
rm -f %{buildroot}%{_mandir}/man8/open_init_pty.8*
rm -f %{buildroot}%{_sbindir}/open_init_pty
rm -f %{buildroot}%{_sbindir}/run_init
rm -f %{buildroot}%{_mandir}/ru/man8/run_init.8*
rm -f %{buildroot}%{_mandir}/man8/run_init.8*
rm -f %{buildroot}/etc/pam.d/run_init*
 
mkdir   -m 755 -p %{buildroot}/%{generatorsdir}
install -m 644 -p %{SOURCE16} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE17} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE18} %{buildroot}/%{_unitdir}/
install -m 755 -p %{SOURCE19} %{buildroot}/%{generatorsdir}/
install -m 755 -p %{SOURCE15} %{buildroot}/%{_libexecdir}/selinux/
 
%find_lang policycoreutils
%find_lang selinux-python
%find_lang selinux-gui
%find_lang selinux-sandbox

%package python-utils
Summary:    SELinux policy core python utilities
Requires:   python-policycoreutils = %{EVRD}
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
Requires:   python-policycoreutils = %{EVRD}
Requires:   python-slip-dbus
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

%package -n python-policycoreutils
%{?python_provide:%python_provide python-policycoreutils}
Summary: SELinux policy core python interfaces
Requires: policycoreutils = %{version}-%{release}
Requires: python-libsemanage >= %{libsemanagever}
Requires: python%{pyver}dist(selinux)
Requires: python-audit >=  %{libauditver}
Requires: checkpolicy
Requires: python-setools >= 4.1.1
BuildArch: noarch

%description -n python-policycoreutils
The python-policycoreutils package contains the interfaces that can be used
by python in an SELinux environment.

%files -f selinux-python.lang -n python-policycoreutils
%{python3_sitelib}/seobject.py*
%{python3_sitelib}/sepolgen
%dir %{python3_sitelib}/sepolicy
%{python3_sitelib}/sepolicy/templates
%dir %{python3_sitelib}/sepolicy/help
%{python3_sitelib}/sepolicy/help/*
%{python3_sitelib}/sepolicy/__pycache__
%{python3_sitelib}/sepolicy/__init__.py*
%{python3_sitelib}/sepolicy/booleans.py*
%{python3_sitelib}/sepolicy/communicate.py*
%{python3_sitelib}/sepolicy/generate.py*
%{python3_sitelib}/sepolicy/interface.py*
%{python3_sitelib}/sepolicy/manpage.py*
%{python3_sitelib}/sepolicy/network.py*
%{python3_sitelib}/sepolicy/transition.py*
%{python3_sitelib}/sepolicy/sedbus.py*
%{python3_sitelib}/sepolicy*.*-info

%package devel
Summary: SELinux policy core policy devel utilities
Requires: policycoreutils-python-utils = %{version}-%{release}
Requires: /usr/bin/make

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
Requires: python-policycoreutils = %{version}-%{release}
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
Requires: policycoreutils-devel = %{EVRD}, python-policycoreutils = %{EVRD}
Requires: policycoreutils-dbus = %{EVRD}
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
%{_datadir}/system-config-selinux/system-config-selinux.png
%{_datadir}/system-config-selinux/*Page.py
%{_datadir}/system-config-selinux/system-config-selinux.py
%{_datadir}/system-config-selinux/*.ui
%{python3_sitelib}/sepolicy/gui.py*
%{python3_sitelib}/sepolicy/sepolicy.glade
%{_datadir}/icons/hicolor/*/apps/sepolicy.png
%{_datadir}/pixmaps/sepolicy.png
%{_mandir}/man8/system-config-selinux.8*
%{_mandir}/man8/selinux-polgengui.8*
%{_mandir}/man8/sepolicy-gui.8*

%files -f %{name}.lang
%{_prefix}/lib/systemd/user/restorecond_user.service
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
%{_mandir}/man8/genhomedircon.8*
%{_mandir}/man5/selinux_config.5.*
%{_mandir}/man5/sestatus.conf.5.*
%{_mandir}/man8/fixfiles.8*
%lang(ru) %{_mandir}/ru/man8/fixfiles.8*
%{_mandir}/man8/load_policy.8*
%lang(ru) %{_mandir}/ru/man8/load_policy.8*
%{_mandir}/man8/restorecon.8*
%lang(ru) %{_mandir}/ru/man8/restorecon.8*
%{_mandir}/man8/restorecon_xattr.8*
%{_mandir}/man8/semodule.8*
%lang(ru) %{_mandir}/ru/man8/semodule.8*
%{_mandir}/man8/sestatus.8*
%lang(ru) %{_mandir}/ru/man8/sestatus.8*
%{_mandir}/man8/setfiles.8*
%lang(ru) %{_mandir}/ru/man8/setfiles.8*
%{_mandir}/man8/setsebool.8*
%lang(ru) %{_mandir}/ru/man8/setsebool.8*
%{_mandir}/man1/secon.1*
%lang(ru) %{_mandir}/ru/man1/secon.1*
%{_mandir}/man8/semodule_expand.8*
%lang(ru) %{_mandir}/ru/man8/semodule_expand.8*
%{_mandir}/man8/semodule_link.8*
%lang(ru) %{_mandir}/ru/man8/semodule_link.8*
%{_mandir}/man8/semodule_unpackage.8*
%{_mandir}/man8/semodule_package.8*
%lang(ru) %{_mandir}/ru/man8/semodule_package.8*
%dir %{_datadir}/bash-completion
%{_datadir}/bash-completion/completions/setsebool
%{!?_licensedir:%global license %%doc}
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
%lang(ru) %{_mandir}/ru/man8/restorecond.8*
%lang(ru) %{_mandir}/ru/man1/audit2why.1*
%lang(ru) %{_mandir}/ru/man1/newrole.1*
%lang(ru) %{_mandir}/ru/man5/sandbox.5*
%lang(ru) %{_mandir}/ru/man5/selinux_config.5*
%lang(ru) %{_mandir}/ru/man5/sestatus.conf.5*
%lang(ru) %{_mandir}/ru/man8/restorecon_xattr.8*
%lang(ru) %{_mandir}/ru/man8/sandbox.8*
%lang(ru) %{_mandir}/ru/man8/selinux-polgengui.8*
%lang(ru) %{_mandir}/ru/man8/semanage-boolean.8*
%lang(ru) %{_mandir}/ru/man8/semanage-dontaudit.8*
%lang(ru) %{_mandir}/ru/man8/semanage-export.8*
%lang(ru) %{_mandir}/ru/man8/semanage-fcontext.8*
%lang(ru) %{_mandir}/ru/man8/semanage-ibendport.8*
%lang(ru) %{_mandir}/ru/man8/semanage-ibpkey.8*
%lang(ru) %{_mandir}/ru/man8/semanage-import.8*
%lang(ru) %{_mandir}/ru/man8/semanage-interface.8*
%lang(ru) %{_mandir}/ru/man8/semanage-login.8*
%lang(ru) %{_mandir}/ru/man8/semanage-module.8*
%lang(ru) %{_mandir}/ru/man8/semanage-node.8*
%lang(ru) %{_mandir}/ru/man8/semanage-permissive.8*
%lang(ru) %{_mandir}/ru/man8/semanage-port.8*
%lang(ru) %{_mandir}/ru/man8/semanage-user.8*
%lang(ru) %{_mandir}/ru/man8/semodule_unpackage.8*
%lang(ru) %{_mandir}/ru/man8/sepolgen.8*
%lang(ru) %{_mandir}/ru/man8/sepolicy-booleans.8*
%lang(ru) %{_mandir}/ru/man8/sepolicy-communicate.8*
%lang(ru) %{_mandir}/ru/man8/sepolicy-generate.8*
%lang(ru) %{_mandir}/ru/man8/sepolicy-gui.8*
%lang(ru) %{_mandir}/ru/man8/sepolicy-interface.8*
%lang(ru) %{_mandir}/ru/man8/sepolicy-manpage.8*
%lang(ru) %{_mandir}/ru/man8/sepolicy-network.8*
%lang(ru) %{_mandir}/ru/man8/sepolicy-transition.8*
%lang(ru) %{_mandir}/ru/man8/sepolicy.8*
%lang(ru) %{_mandir}/ru/man8/seunshare.8*
%lang(ru) %{_mandir}/ru/man8/system-config-selinux.8*

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
