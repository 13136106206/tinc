Summary: tinc vpn daemon
Name: tinc
Version: 1.0
Release: pre1
Copyright: GPL
Group: Networking
URL: http://tinc.nl.linux.org/
Source0: %{name}-%{version}.tar.gz
Buildroot: /var/tmp/%{name}-%{version}-%{release}
Requires: /usr/bin/texi2html /usr/bin/install /usr/bin/patch

%description
tinc is cool!
See http://tinc.nl.linux.org/

%prep

%setup -q -n %{name}-%{version}

%build
#autoconf
#automake
./configure --prefix=/usr --sysconfdir=/etc
make
texi2html doc/tinc.texi

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -D redhat/tinc $RPM_BUILD_ROOT/etc/rc.d/init.d/

ME=my.vpn.ip.number
PEER=peer.vpn.ip.number
PEEREAL=peer.real.ip.number

mkdir -p $RPM_BUILD_ROOT/etc/tinc/$PEER/passphrases
cat <<END >$RPM_BUILD_ROOT/etc/tinc/$PEER/tincd.conf
#sample
TapDevice = /dev/tap0
ConnectTo = $PEEREAL
MyVirtualIP = $ME/32
AllowConnect = no
END
cat <<END >$RPM_BUILD_ROOT/etc/tinc/$PEER/passphrases/local
128 0c647a1fd34da9d04c1d340ae9363f31
END
cat <<END >$RPM_BUILD_ROOT/etc/tinc/$PEER/passphrases/$PEER
128 aea5a5d414fea63ee3829b592afc0fba
END

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%post

/sbin/chkconfig --add tinc

grep -q '^tinc[[:space:]]' /etc/services || patch -s /etc/services << END
*** services.org        Tue Apr 18 13:22:22 2000
--- services    Tue Apr 18 13:24:19 2000
***************
*** 145,148 ****
--- 145,150 ----
  hmmp-ind	612/tcp		dqs313_intercell# HMMP Indication / DQS
  hmmp-ind	612/udp		dqs313_intercell# HMMP Indication / DQS
+ tinc		655/tcp		TINC		# tinc vpn
+ tinc		655/udp		TINC		# tinc.nl.linux.org
  #
  # UNIX specific services
END

%preun
%postun

%files

%doc AUTHORS ChangeLog NEWS README THANKS TODO *.html

#%defattr(-,root,root)
%config /etc/tinc
/etc/rc.d
/usr/sbin
/usr/lib/tinc
/usr/man
/usr/info

%changelog
* Tue Apr 18 2000 Mads Kiileric <mads@kiilerich.com>
- initial rpm
