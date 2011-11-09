%include fedora-live-desktop.ks

firewall --disabled
selinux --disabled
repo --name=euca --baseurl=http://downloads.eucalyptus.com/software/devel/fedora-16/2.0.3-live/x86_64/

%packages
@editors
qemu-kvm
libvirt
keyutils
iscsi-initiator-utils
trousers
bridge-utils
fipscheck
device-mapper-multipath
eucalyptus-cloud
eucalyptus-walrus
eucalyptus-nc
eucalyptus-sc
eucalyptus-cc
eucalyptus-gl
eucalive-firstboot
euca2ools
java-1.6.0-openjdk-devel
java-1.6.0-openjdk
perl-Crypt-OpenSSL-Random
vblade
ntp
perl-DBI
python-boto
bridge-utils
syslinux
system-config-firewall-base
system-config-network
firefox
python-netaddr
gdm
generic-logos
generic-release
generic-release-notes
-fedora-logos
-fedora-release
-fedora-release-notes
-evolution
-evolution-NetworkManager
-evolution-help
-gnome-games
-aisleriot
-smolt-firstboot
%end

%post
cat <<EOF >>/etc/libvirt/libvirtd.conf
unix_sock_group = "kvm"
unix_sock_ro_perms = "0777"
unix_sock_rw_perms = "0770"
EOF

/usr/sbin/usermod -G kvm eucalyptus
sed -i -r 's/^(Default.*requiretty)/# \1/' /etc/sudoers

# This isn't great, but it's a livecd...
echo "liveuser	ALL=NOPASSWD: ALL" >> /etc/sudoers

# remove firstboot modules that we don't want
rm -f /usr/share/firstboot/modules/{create_user,date,eula,keyboard,welcome}.py*

%end
