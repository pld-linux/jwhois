Summary:	The GNU Whois client
Summary(pl):	Klient Whois z GNU
Name:		jwhois
Version:	3.2.2
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	ftp://ftp.gnu.org/gnu/jwhois/%{name}-%{version}.tar.gz
# Source0-md5:	3ad57a8cfc4f32fe41b1131711d34a78
Patch0:		%{name}-info.patch
Patch1:		%{name}-nolibs.patch
URL:		http://www.gnu.org/software/jwhois/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdbm-devel
BuildRequires:	gettext-devel
BuildRequires:	texinfo
Requires(pre,preun):	fileutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir	/var/cache/jwhois
%define		cachegrp	nobody

%description
JWHOIS is an Internet Whois client that queries hosts for information
according to RFC 954 - NICNAME/WHOIS. JWHOIS is configured via a
configuration file that contains information about all known Whois
servers. Upon execution, the host to query is selected based on the
information in the configuration file.

The configuration file is highly customizable and makes heavy use of
regular expressions.

%description -l pl
JWHOIS to klient internetowej us³ugi Whois, odpytuj±cy hosty o
informacje zgodnie z RFC 954 - NICNAME/WHOIS. JWOIS jest konfigurowany
poprzez plik zawieraj±cy informacje o wszystkich znanych serwerach
Whois. Podczas wykonywania programu host do odpytania jest wybierany
na podstawie informacji z pliku konfiguracyjnego.

Plik konfiguracyjny daje du¿e mo¿liwo¶ci konfiguracji i intensywnie
wykorzystuje wyra¿enia regularne.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-GROUP=%{cachegrp}

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
[ -f %{_localstatedir}/jwhois.db ] && rm -f %{_localstatedir}/jwhois.db

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%preun
if [ "$1" = "0" ]; then
	[ -f %{_localstatedir}/jwhois.db ] && rm -f %{_localstatedir}/jwhois.db
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jwhois.conf
%attr(2755,root,%{cachegrp}) %{_bindir}/jwhois
%{_mandir}/man1/jwhois.1*
%lang(sv) %{_mandir}/sv/man1/jwhois.1*
%{_infodir}/jwhois.info*
%attr(775,root,%{cachegrp}) %dir %{_localstatedir}
