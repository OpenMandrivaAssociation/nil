%define name	nil
%define title	NiL
%define version	000516
%define release %mkrel 24
%define prefix	%{_prefix}
%define summary	%{title} Isn't Liero
%define group	Games/Arcade
%define icon	%{name}.png

Summary:	%{summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		%{group}
Source:		http://dl.sf.net/nil/%{name}-%{version}.tar.bz2
Source10:	%{name}.16.png.bz2
Source11:	%{name}.32.png.bz2
Source12:	%{name}.48.png.bz2
Patch0:		nil-add-pkgdatadir.patch
Patch1:		nil-000516-i18ned-keys.patch
Patch2:		nil-remove-debug-printings.patch
Patch3: nil-000516-gcc31.patch
Patch4:		nil-64.patch
Patch5:		nil-000516-gcc43.patch
URL:		http://nil.sf.net/
BuildRequires:	SDL-devel 
BuildRequires:  SDL_mixer-devel 
BuildRequires:  X11-devel 
BuildRequires:  zlib-devel
BuildRequires:  automake1.4
BuildRequires:  autoconf2.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	common-licenses

%description
The game itself can be described either as Quake in 2D or worms done right
(ie not turn based), the basic game play is kill kill kill, with a wide
selection of interesting weapons.

Porting apparently wasn't much of a priority for the authour, so I set
about reimplementing it on Linux.

%prep
%setup -q -n %{name}
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p1
%patch5 -p1
# remove nasty no-newline-at-end-of-line, it bothers gcc-2.96
find . -name "*.h" -exec perl -pi -e '$_.="\n" if eof' {} \;

%build
cd nil
autoconf-2.13
automake-1.4 -a
%configure
make

%install
mkdir -p %{buildroot}{%{_bindir},%{_datadir}/nil}
cp nil/nil/nil %{buildroot}/%{_bindir}
cp -a gfx %{buildroot}/%{_datadir}/nil
rm -rf %{buildroot}/%{_datadir}/nil/gfx/{CVS,*/CVS,*/*/CVS,*/*/*/CVS}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name}
Icon=%{icon}  
Categories=Game;ArcadeGame;
Name=%{title}  
Comment=%{summary}
EOF

mkdir -p %{buildroot}{%{_iconsdir},%{_liconsdir},%{_miconsdir}}
bzcat %{SOURCE10} > %{buildroot}%{_miconsdir}/%{icon}
bzcat %{SOURCE11} > %{buildroot}%{_iconsdir}/%{icon}
bzcat %{SOURCE12} > %{buildroot}%{_liconsdir}/%{icon}

rm -rf %{buildroot}%{_datadir}/nil/gfx/original/fonts/ttf

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc README AUTHORS docs/*.txt docs/TODO
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{icon}
%{_iconsdir}/%{icon}
%{_liconsdir}/%{icon}


