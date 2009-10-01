%define major     0
%define libname   %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name: nbtk
Summary: Experiemental toolkit for Moblin
Group: System/Libraries
Version: 1.1.4
License: LGPLv2.1
URL: http://www.moblin.org
Release: %mkrel 1
Source0: http://git.moblin.org/cgit.cgi/%{name}/snapshot/%{name}-%{version}.tar.bz2
Patch0: nbtk-1.1.4-libccss-dependency.patch
Patch1: nbtk-1.1.4-libccss-fix.patch 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: clutter-devel
BuildRequires: libccss-devel
BuildRequires: libglib2.0-devel
BuildRequires: libgtk+2.0-devel
BuildRequires: gir-repository
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel
BuildRequires: pkgconfig

%description
NBTK is a currently experimental toolkit for Moblin

%package -n %{libname}
Summary: NBTK libraries
Group: System/Libraries

%description -n %{libname}
NBTK is a currently experimental toolkit for Moblin

%package -n nbtk-doc

Summary: NBTK documentation
Group: System/Libraries

%description -n nbtk-doc
Documentation for NBTK

%package -n %{develname}

Summary: NBTK development libraries and headers
Group: System/Libraries

Requires: %{libname} = %{version}-%{release}
Requires: pkgconfig
Requires: %{libname} >= %{version}

%description -n %{develname} 
NBTK development libraries and header files

%package -n libnbtk-gtk

Summary: NBTK GTK+ support
Group: System/Libraries

Requires: %{libname} = %{version}-%{release}
Requires: pkgconfig
Requires: %{libname} >= %{version}

%description -n libnbtk-gtk
NBTK GTK+ support

%prep
%setup -q -n nbtk-%{version}
%patch0 -p0
%patch1 -p1

%build
./autogen.sh
%configure2_5x --enable-gtk-doc
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}-%{version}
for f in `ls %{buildroot}/%{_datadir}/doc/`; do
	if [ -f %{buildroot}/%{_datadir}/doc/$f ]; then
		mv %{buildroot}/%{_datadir}/doc/$f %{buildroot}/%{_datadir}/doc/%{name}-%{version}
	fi
done

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,-)
%doc NEWS README HACKING ChangeLog COPYING.LIB AUTHORS
%{_bindir}/*
%{_libdir}/libnbtk-1.2.so.%{major}*
%{_datadir}/locale/*
%{_datadir}/nbtk/style/*

%files -n nbtk-doc
%defattr(-,root,root,-)
/usr/share/gtk-doc/html/nbtk

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/nbtk-1.2/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*
%{_libdir}/girepository-1.0/
%{_libdir}/libnbtk-gtk-1.2.la
%{_libdir}/libnbtk-gtk-1.2.so
%{_libdir}/libnbtk-1.2.la

%files -n libnbtk-gtk
%{_libdir}/libnbtk-gtk*.so.%{major}*
