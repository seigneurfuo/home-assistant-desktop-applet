Name:           home-assistant-indicator
Version:        2024.02.03
Release:        %autorelease
BuildArch:      noarch
Summary:        Application en zone de notification pour monter les différents capteurs d'une instance Home Assistant

License:        None
URL:            http://seigneurfuo.com

Requires:       python3
Requires:       python3-PyQt6
Requires:       python3-requests

%description
Application en zone de notification pour monter les différents capteurs d'une instance Home Assistant

%install
# Programme
mkdir -p %{buildroot}/%{_bindir}
install -m 755 ../../src/app.py %{buildroot}/%{_bindir}/%{name}.py

# Racourci
mkdir -p %{buildroot}/usr/share/applications/
install -m 644 ./%{name}.desktop %{buildroot}/usr/share/applications/%{name}.desktop

# Autostart
mkdir -p %{buildroot}/etc/xdg/autostart/
install -m 644 ./%{name}-autostart.desktop %{buildroot}/etc/xdg/autostart/%{name}.desktop

%files
%{_bindir}/%{name}.py
/usr/share/applications/%{name}.desktop
/etc/xdg/autostart/%{name}.desktop
