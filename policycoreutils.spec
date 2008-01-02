%define        libauditver        1.4.2-1
%define        libsepolver        2.0.10-1
%define        libsemanagever        2.0.5-1
%define        libselinuxver        2.0.34-1
%define        sepolgenver        1.0.10
Summary: SELinux policy core utilities

Name:         policycoreutils
Version: 2.0.34
Release: %mkrel 1
License: GPLv2+
Group:         System/Base
Source:         http://www.nsa.gov/selinux/archives/policycoreutils-%{version}.tgz
Source1: http://www.nsa.gov/selinux/archives/sepolgen-%{sepolgenver}.tgz
URL:         http://www.selinuxproject.org
Source2: system-config-selinux.png
Source3: system-config-selinux.desktop
Source4: system-config-selinux.pam
Source5: system-config-selinux.console
Source6: selinux-polgengui.desktop
Source7: selinux-polgengui.console
Source8: policycoreutils_man_ru2.tar.bz2
Patch:         policycoreutils-rhat.patch
Patch1:         policycoreutils-po.patch
#Patch2: policycoreutils-sepolgen.patch
Patch3:         policycoreutils-gui.patch
Patch4:         policycoreutils-sepolgen.patch

BuildRequires: pam-devel sepol-devel >= %{libsepolver} semanage-devel >= %{libsemanagever} selinux-devel >= %{libselinuxver} cap-devel audit-libs-devel >=  %{libauditver} gettext
Requires: /bin/mount /bin/egrep /bin/awk /usr/bin/diff rpm /bin/sed 
#Requires: selinux >=  %{libselinuxver} sepol >= %{libsepolver} semanage >= %{libsemanagever} coreutils audit-libs-python >=  %{libauditver} checkpolicy selinux-python
Requires(post): /sbin/service /sbin/chkconfig 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

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
to switch roles, and run_init to run /etc/init.d scripts in the proper
context.

%prep
%setup -q -a 1 
%patch -p1 -b .rhat
%patch1 -p1 -b .rhatpo
#%patch2 -p1 -b .sepolgen
%patch3 -p1 -b .gui
%patch4 -p1 -b .sepolgen

%build
make LSPP_PRIV=y LIBDIR="%{_libdir}" CFLAGS="%{optflags} -fPIE" LDFLAGS="-pie -Wl,-z,relro" all 
make -C sepolgen-%{sepolgenver} LSPP_PRIV=y LIBDIR="%{_libdir}" CFLAGS="%{optflags} -fPIE" LDFLAGS="-pie -Wl,-z,relro" all 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps

make LSPP_PRIV=y  DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" install
make -C sepolgen-%{sepolgenver} DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" install

install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/system-config-selinux/
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/system-config-selinux
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/selinux-polgengui
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/security/console.apps/system-config-selinux
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/security/console.apps/selinux-polgengui
tar -jxf %{SOURCE8} -C %{buildroot}/
ln -sf consolehelper %{buildroot}%{_bindir}/system-config-selinux
ln -sf consolehelper %{buildroot}%{_bindir}/selinux-polgengui

desktop-file-install --vendor fedora \
                     --dir ${RPM_BUILD_ROOT}%{_datadir}/applications        \
                     --add-category X-Fedora                                \
                     %{SOURCE3}

desktop-file-install --vendor fedora \
                     --dir ${RPM_BUILD_ROOT}%{_datadir}/applications        \
                     --add-category X-Fedora                                \
                     %{SOURCE6}
%find_lang %{name}

%package newrole
Summary: The newrole application for RBAC/MLS 
Group: System/Base
Requires: policycoreutils = %{version}-%{release} 

%description newrole
RBAC/MLS policy machines require newrole as a way of changing the role 
or level of a logged in user.

%files newrole
%attr(4755,root,root) %{_bindir}/newrole
%{_mandir}/man1/newrole.1*

%package gui
Summary: SELinux configuration GUI
Group: System/Base
Requires: policycoreutils = %{version}-%{release} 
Requires: gnome-python, pygtk2, python-gtk-glade, gnome-python-canvas
Requires: usermode-consoleonly, rhpl
Requires: python >= 2.4
BuildRequires: desktop-file-utils
Requires: selinux-policy-devel

%description gui
system-config-selinux is a utility for managing the SELinux environment

%files gui
%{_bindir}/system-config-selinux
%{_bindir}/selinux-polgengui
%{_datadir}/applications/fedora-system-config-selinux.desktop
%{_datadir}/applications/fedora-selinux-polgengui.desktop
%dir %{_datadir}/system-config-selinux
%dir %{_datadir}/system-config-selinux/templates
%{_datadir}/system-config-selinux/*.py*
%{_datadir}/system-config-selinux/selinux.tbl
%{_datadir}/system-config-selinux/*png
%{_datadir}/system-config-selinux/*.glade
%{_datadir}/system-config-selinux/templates/*.py*
%config(noreplace) %{_sysconfdir}/pam.d/system-config-selinux
%config(noreplace) %{_sysconfdir}/pam.d/selinux-polgengui
%config(noreplace) %{_sysconfdir}/security/console.apps/system-config-selinux
%config(noreplace) %{_sysconfdir}/security/console.apps/selinux-polgengui

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/sbin/restorecon
/sbin/fixfiles
/sbin/setfiles
%{_sbindir}/genhomedircon
%{_sbindir}/restorecond
%{_sbindir}/setsebool
%{_sbindir}/semodule
%{_sbindir}/semanage
%{_sbindir}/load_policy
%{_sbindir}/sestatus
%{_sbindir}/run_init
%{_sbindir}/open_init_pty
%{_bindir}/sepolgen-ifgen
%{_bindir}/audit2allow
%{_bindir}/audit2why
%{_bindir}/chcat
%{_bindir}/secon
%{_bindir}/semodule_deps
%{_bindir}/semodule_expand
%{_bindir}/semodule_link
%{_bindir}/semodule_package
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_mandir}/ru/*/*
%config(noreplace) %{_sysconfdir}/pam.d/newrole
%config(noreplace) %{_sysconfdir}/pam.d/run_init
%config(noreplace) %{_sysconfdir}/sestatus.conf
%{_libdir}/python?.?/site-packages/seobject.py*
%attr(755,root,root) /etc/rc.d/init.d/restorecond
%config(noreplace) /etc/selinux/restorecond.conf
%dir %{_libdir}/python?.?/site-packages/sepolgen
%{_libdir}/python?.?/site-packages/sepolgen/*
%dir  /var/lib/sepolgen
/var/lib/sepolgen/perm_map

%preun
if [ $1 -eq 0 ]; then
   /sbin/service restorecond stop > /dev/null 2>&1
   /sbin/chkconfig --del restorecond
fi

%post
/sbin/chkconfig --add restorecond
[ -f /usr/share/selinux/devel/include/build.conf ] && /usr/bin/sepolgen-ifgen  > /dev/null 
/usr/bin/sepolgen-ifgen  > /dev/null
exit 0

%postun
if [ "$1" -ge "1" ]; then 
   [ -x /sbin/service ] && /sbin/service restorecond condrestart  > /dev/null
fi

