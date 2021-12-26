#
# Conditional build:
%bcond_without	gegl	# build without GeGL
%bcond_without	openmp	# OpenMP threading support
%bcond_without	opencl	# OpenCL support
%bcond_with	vte	# lighttable mode shell ("file manager" April fool)

Summary:	darktable - a virtual lighttable and darkroom for photographers
Summary(pl.UTF-8):	darktable - wirtualny podświetlany stół i ciemnia dla fotografów
Name:		darktable
Version:	3.8.0
Release:	1
License:	GPL v3
Group:		X11/Applications/Graphics
Source0:	https://github.com/darktable-org/darktable/releases/download/release-%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	7164bb403ac9741e157d7763310c445a
Patch0:		cmake-glib.patch
URL:		https://www.darktable.org/
BuildRequires:	GraphicsMagick-devel
%{?with_opencl:BuildRequires:	OpenCL-devel}
BuildRequires:	OpenEXR-devel >= 2.0
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel >= 1.2
BuildRequires:	cairo-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	colord-devel
BuildRequires:	colord-gtk-devel
BuildRequires:	cups-devel
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	dbus-glib-devel >= 0.80
BuildRequires:	desktop-file-utils
BuildRequires:	exiv2-devel >= 0.24
BuildRequires:	flickcurl-devel
BuildRequires:	fop
%{?with_openmp:BuildRequires:	gcc-c++ >= 6:4.3}
BuildRequires:	gdk-pixbuf2-devel >= 2
%{?with_gegl:BuildRequires:	gegl-devel}
BuildRequires:	gettext
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.30
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	intltool
BuildRequires:	iso-codes >= 4.4
BuildRequires:	json-glib-devel
BuildRequires:	lcms2-devel >= 2
BuildRequires:	lensfun-devel
BuildRequires:	libglade2-devel
BuildRequires:	libgnome-keyring-devel
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libgphoto2-devel >= 2.4.5
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel >= 1:2.26
BuildRequires:	libsoup-devel >= 2
BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel >= 0.3.0
BuildRequires:	libxml2-devel >= 1:2.6
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	llvm-devel >= 12.0
BuildRequires:	lua54-devel >= 5.4
BuildRequires:	openjpeg-devel >= 1.5.0
BuildRequires:	pango-devel
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	po4a
BuildRequires:	pugixml-devel >= 1.8
BuildRequires:	sqlite3-devel >= 3.24
BuildRequires:	squish-devel
%{?with_vte:BuildRequires:	vte-devel >= 0.26.0}
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	curl >= 7.18.0
Requires:	dbus-glib >= 0.80
Requires:	glib2 >= 1:2.30
Requires:	gtk+3 >= 3.22
Requires:	openjpeg >= 1.5.0
%{?with_vte:Requires:	vte >= 0.26.0}
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
darktable is a virtual lighttable and darkroom for photographers.

%description -l pl.UTF-8
darktable to wirtualny podświetlany stół i ciemnia dla fotografów.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
export CXXFLAGS="%{rpmcxxflags}"
%cmake .. \
	-DCMAKE_BUILD_TYPE=%{!?debug:RELEASE}%{?debug:DEBUG} \
	%{?with_vte:-DAPRIL_FOOLS=ON} \
	-DBINARY_PACKAGE_BUILD=ON \
	-DPROJECT_VERSION:STRING="%{version}" \
	-DUSE_AVIF=OFF \
	%{!?with_opencl:-DUSE_OPENCL=OFF} \
	%{!?with_openmp:-DUSE_OPENMP=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/%{name}" >$RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}.conf
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING.md README.md RELEASE_NOTES.md
%doc doc/{TRANSLATORS.md,grouping.txt,thumbnail_color_management.txt}
%attr(755,root,root) %{_bindir}/darktable
%attr(755,root,root) %{_bindir}/darktable-chart
%attr(755,root,root) %{_bindir}/darktable-cli
%attr(755,root,root) %{_bindir}/darktable-cltest
%attr(755,root,root) %{_bindir}/darktable-cmstest
%attr(755,root,root) %{_bindir}/darktable-generate-cache
%attr(755,root,root) %{_bindir}/darktable-rs-identify
/etc/ld.so.conf.d/%{name}.conf
%{_datadir}/metainfo/darktable.appdata.xml
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
%lang(de) %{_mandir}/de/man1/darktable.1*
%lang(de) %{_mandir}/de/man1/darktable-cli.1*
%lang(de) %{_mandir}/de/man1/darktable-cltest.1*
%lang(de) %{_mandir}/de/man1/darktable-cmstest.1*
%lang(de) %{_mandir}/de/man1/darktable-generate-cache.1*
%lang(es) %{_mandir}/es/man1/darktable.1*
%lang(es) %{_mandir}/es/man1/darktable-cli.1*
%lang(es) %{_mandir}/es/man1/darktable-cltest.1*
%lang(es) %{_mandir}/es/man1/darktable-cmstest.1*
%lang(es) %{_mandir}/es/man1/darktable-generate-cache.1*
%lang(fr) %{_mandir}/fr/man1/darktable.1*
%lang(fr) %{_mandir}/fr/man1/darktable-cli.1*
%lang(fr) %{_mandir}/fr/man1/darktable-cltest.1*
%lang(fr) %{_mandir}/fr/man1/darktable-cmstest.1*
%lang(fr) %{_mandir}/fr/man1/darktable-generate-cache.1*
%{_mandir}/man1/darktable.1*
%{_mandir}/man1/darktable-cli.1*
%{_mandir}/man1/darktable-cltest.1*
%{_mandir}/man1/darktable-cmstest.1*
%{_mandir}/man1/darktable-generate-cache.1*
