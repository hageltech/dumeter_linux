%define name dumeter-reporter
%define version 1.0
%define release 1

Summary: Network bandwidth usage reporter for dumeter.net service.
Name: %{name}
Version: %{version}
Release: %{release}
URL: https://www.dumeter.net/
Source0: %{name}-%{version}.tar.gz
Source1: dumeter-reporter.service
License: Mozilla Public License Version 2.0 (MPL-2.0)
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Hagel Technologies Ltd. <support@hageltech.com>
BuildRequires: systemd
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Network bandwidth usage reporter for dumeter.net service.
dumeter.net provides a comprehensive view of your Internet bandwidth
utilization, across all your computers. Avoid overage charges, throttling,
and other "niceties" of capped or metered Internet connection.

%prep
%setup -n %{name}-%{version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --install-lib=/usr/share/dumeter-reporter --install-scripts=/usr/sbin
rm $RPM_BUILD_ROOT/usr/share/dumeter-reporter/*.egg-info
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/dumeter-reporter.service

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group dureporter >/dev/null 2>&1 || groupadd -r dureporter
getent passwd dureporter >/dev/null 2>&1 || \
    useradd -r -g dureporter -d /var/lib/dumeter-reporter -s /sbin/nologin \
    	-c "dumeter.net reporter" dureporter >/dev/null 2>&1 || exit 1
chown -R dureporter:dureporter /var/lib/dumeter-reporter >/dev/null 2>&1
exit 0

%post
%systemd_post dumeter-reporter.service

%preun
%systemd_preun dumeter-reporter.service

%postun
%systemd_postun_with_restart dumeter-reporter.service
rm -f /var/lib/dumeter-reporter/db.sqlite
rmdir --ignore-fail-on-non-empty /var/lib/dumeter-reporter
userdel dureporter >/dev/null 2>&1 || true
groupdel dureporter >/dev/null 2>&1 || true

%files
%defattr(-,root,root)
%{_unitdir}/dumeter-reporter.service
%doc README* LICENSE.txt
%config(noreplace) %{_sysconfdir}/dumeter-reporter.conf
%{_sbindir}/dumeter-reporter
%{_datarootdir}/dumeter-reporter/dumeter/*.py*
%attr(0750,dureporter,dureporter) %dir /var/lib/dumeter-reporter

%changelog

* Fri May 29 2015 Haim Gelfenbeyn <haim@hageltech.com>
- Initial release of dumeter.net reporter for Linux.
