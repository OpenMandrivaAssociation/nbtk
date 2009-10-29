%define version 1.1.13
%define rel 1
%define snapdate 0
# 20091029

# they didn't tagged it properly, even misnamed the version
%define snapshot 4039bcea9729ec9709c93dc6d0076dbd43fde5a5

%if %{snapdate}
%define release %mkrel 0.%{snapdate}.%{rel}
%else
%define release %mkrel %{rel}
%endif

%define major     0
%define libname   %mklibname %{name} %{major}
%define gtklibname   %mklibname %{name}-gtk %{major}
%define develname %mklibname %{name} -d

Name: nbtk
Summary: Experimental toolkit for Moblin
Group: System/Libraries
Version: %{version}
License: LGPLv2.1
URL: http://www.moblin.org
Release: %{release}
Source0: http://git.moblin.org/cgit.cgi/%{name}/snapshot/%{name}-%{snapshot}.tar.gz
Patch0: 01_use_ccss0.5.0.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: clutter-devel
BuildRequires: libccss-devel
BuildRequires: clutter-imcontext-devel
BuildRequires: libglib2.0-devel
BuildRequires: libgtk+2.0-devel
BuildRequires: gir-repository
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel

%description
NBTK is a currently experimental toolkit for Moblin

%package -n %{libname}
Summary: NBTK libraries
Group: System/Libraries
Requires: %{name}

%description -n %{libname}
NBTK is a currently experimental toolkit for Moblin

%package -n nbtk-doc

Summary: NBTK documentation
Group: System/Libraries

%description -n nbtk-doc
Documentation for NBTK

%package -n %{develname}

Summary: NBTK development libraries and headers
Group: Development/C

Requires: %{libname} = %{version}-%{release}
Requires: %{gtklibname} = %{version}-%{release}
Provides: %{name}-devel

%description -n %{develname} 
NBTK development libraries and header files

%package -n %{gtklibname}

Summary: NBTK GTK+ support
Group: System/Libraries

Requires: %{libname} = %{version}-%{release}
Requires: pkgconfig
Requires: %{libname} >= %{version}

%description -n %{gtklibname}
NBTK GTK+ support

%prep
%setup -q -n %{name}-%{snapshot}
%patch0 -p1 -b .ccss050
perl -pi -e 's,^\$srcdir/configure,/bin/true,' ./autogen.sh

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

%files
%defattr(-,root,root,-)
%doc NEWS README HACKING ChangeLog COPYING.LIB AUTHORS
%{_bindir}/*
%{_datadir}/locale/*
%{_datadir}/nbtk/style/*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libnbtk-1.2.so.%{major}*

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
%{_libdir}/libnbtk-1.2.so

%files -n %{gtklibname}
%{_libdir}/libnbtk-gtk*.so.%{major}*
