%global initdir /etc/init.d

Name:           eucalive-firstboot
Version:        1.0
Release:        2%{?dist}
Summary:        Firstboot screen for Eucalyptus configuration

Group:          Applications/Internet
License:        GPL
URL:            http://open.eucalyptus.com 
Source0:        firstboot-eucalive.py
Source1:        register-euca-components.init
BuildArch:      noarch
Requires:       firstboot

%description
This provides firstboot integration for the Eucalyptus liveCD,
and an init script to subsequntly register Eucalyptus components.

%prep

%build

%install
mkdir -p ${RPM_BUILD_ROOT}/%{_datadir}/firstboot/modules/
cp %{S:0} ${RPM_BUILD_ROOT}/%{_datadir}/firstboot/modules/euca.py
mkdir -p ${RPM_BUILD_ROOT}/%{initdir}
cp %{S:1} ${RPM_BUILD_ROOT}/%{initdir}/register-euca-components
chmod +x ${RPM_BUILD_ROOT}/%{initdir}/register-euca-components

%post
chkconfig --add register-euca-components

%files
%{_datadir}/firstboot/modules/euca.py*
%{initdir}/register-euca-components

%changelog
* Tue Nov  8 2011 Andy Grimm <agrimm@gmail.com> - 1.0-2
- initial package
