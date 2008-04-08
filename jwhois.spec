Summary:	The GNU Whois client
Summary(pl.UTF-8):	Klient Whois z GNU
Name:		jwhois
Version:	4.0
Release:	1
License:	GPL v3+
Group:		Networking/Utilities
Source0:	http://ftp.gnu.org/gnu/jwhois/%{name}-%{version}.tar.gz
# Source0-md5:	977d0ba90ee058a7998c94d933fc9546
Patch0:		%{name}-info.patch
Patch1:		%{name}-nolibs.patch
Patch2:		%{name}-pl.po-update.patch
URL:		http://www.gnu.org/software/jwhois/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gdbm-devel
BuildRequires:	gettext-devel
BuildRequires:	rpmbuild(macros) >= 1.159
BuildRequires:	texinfo
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre,preun):	fileutils
Provides:	group(whois)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir	/var/cache/jwhois

%description
JWHOIS is an Internet Whois client that queries hosts for information
according to RFC 954 - NICNAME/WHOIS. JWHOIS is configured via a
configuration file that contains information about all known Whois
servers. Upon execution, the host to query is selected based on the
information in the configuration file.

The configuration file is highly customizable and makes heavy use of
regular expressions.

%description -l pl.UTF-8
JWHOIS to klient internetowej usługi Whois, odpytujący hosty o
informacje zgodnie z RFC 954 - NICNAME/WHOIS. JWOIS jest konfigurowany
poprzez plik zawierający informacje o wszystkich znanych serwerach
Whois. Podczas wykonywania programu host do odpytania jest wybierany
na podstawie informacji z pliku konfiguracyjnego.

Plik konfiguracyjny daje duże możliwości konfiguracji i intensywnie
wykorzystuje wyrażenia regularne.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

rm -f po/stamp-po

%build
%{__gettextize}
%{__aclocal} -I m4 -I gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-GROUP=whois

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_localstatedir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Modify and install jwhois.conf
sed -e 's@^#cachefile.*$@cachefile = "%{_localstatedir}/jwhois.db";@g' \
	-e 's@^#cacheexpire.*$@cacheexpire = 24;@g' example/jwhois.conf \
	> $RPM_BUILD_ROOT%{_sysconfdir}/jwhois.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 87 whois
[ -f %{_localstatedir}/jwhois.db ] && rm -f %{_localstatedir}/jwhois.db

%post	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%preun
if [ "$1" = "0" ]; then
	[ -f %{_localstatedir}/jwhois.db ] && rm -f %{_localstatedir}/jwhois.db
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
if [ "$1" = "0" ]; then
	%groupremove whois
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jwhois.conf
%attr(2755,root,whois) %{_bindir}/jwhois
%{_mandir}/man1/jwhois.1*
%lang(sv) %{_mandir}/sv/man1/jwhois.1*
%{_infodir}/jwhois.info*
%attr(775,root,whois) %dir %{_localstatedir}
