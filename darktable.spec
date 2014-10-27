#
# Conditional build:
%bcond_without	gegl	# build without GeGL

Summary:	darktable is a virtual lighttable and darkroom for photographers
Summary(pl.UTF-8):	darktable to wirtualny podświetlany stół i ciemnia dla fotografów
Name:		darktable
Version:	1.4
Release:	7
License:	GPL v3
Group:		X11/Applications/Graphics
Source0:	http://downloads.sourceforge.net/darktable/%{name}-%{version}.tar.xz
# Source0-md5:	896416931ded4579f528cd11edad470c
Patch0:		cmake-glib.patch
URL:		http://darktable.sourceforge.net/
BuildRequires:	GraphicsMagick-devel
BuildRequires:	OpenEXR-devel >= 2.0
BuildRequires:	SDL-devel
BuildRequires:	cairo-devel
BuildRequires:	cmake
BuildRequires:	colord-devel
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	dbus-glib-devel >= 0.80
BuildRequires:	desktop-file-utils
BuildRequires:	exiv2-devel
BuildRequires:	flickcurl-devel
BuildRequires:	fop
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk+2-devel
BuildRequires:	intltool
BuildRequires:	lcms2-devel
BuildRequires:	lensfun-devel
BuildRequires:	libglade2-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libgomp-devel
BuildRequires:	libgphoto2-devel >= 2.4.5
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel >= 1:2.26
BuildRequires:	libtiff-devel
BuildRequires:	lua52-devel
BuildRequires:	pkgconfig >= 0.22
BuildRequires:	sqlite-devel
BuildRequires:	sqlite3-devel
%if %{with gegl}
BuildRequires:	gegl-devel
%endif
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
darktable is a virtual lighttable and darkroom for photographers

%description -l pl.UTF-8
darktable to wirtualny podświetlany stół i ciemnia dla fotografów

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_LIBRARY_PATH:PATH=%{_libdir} \
	-DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
	-DBINARY_PACKAGE_BUILD=1 \
	-DPROJECT_VERSION:STRING="%{name}-%{version}-%{release}" \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%{__mv} $RPM_BUILD_ROOT%{_localedir}/pt{_PT,}

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/README doc/AUTHORS doc/LICENSE doc/TRANSLATORS
%attr(755,root,root) %{_bindir}/darktable
%attr(755,root,root) %{_bindir}/darktable-cli
%attr(755,root,root) %{_bindir}/darktable-cltest
%attr(755,root,root) %{_bindir}/darktable-viewer
%{_datadir}/appdata/darktable.appdata.xml
%{_datadir}/darktable
%{_desktopdir}/darktable.desktop
%{_iconsdir}/hicolor/*/apps/darktable.png
%{_iconsdir}/hicolor/scalable/apps/darktable*.svg
%dir %{_libdir}/darktable
%dir %{_libdir}/darktable/plugins
%dir %{_libdir}/darktable/plugins/imageio
%dir %{_libdir}/darktable/plugins/imageio/format
%dir %{_libdir}/darktable/plugins/imageio/storage
%dir %{_libdir}/darktable/plugins/lighttable
%dir %{_libdir}/darktable/views
%attr(755,root,root) %{_libdir}/darktable/libdarktable.so
%attr(755,root,root) %{_libdir}/darktable/plugins/*.so
%attr(755,root,root) %{_libdir}/darktable/plugins/imageio/format/*.so
%attr(755,root,root) %{_libdir}/darktable/plugins/imageio/storage/*.so
%attr(755,root,root) %{_libdir}/darktable/plugins/lighttable/*.so
%attr(755,root,root) %{_libdir}/darktable/views/*.so
%{_mandir}/man1/darktable.1*
%{_mandir}/man1/darktable-cli.1*
