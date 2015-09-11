import os
from django.conf import settings
from pipeline.compilers import CompilerBase
import sass


class LibSassCompiler(CompilerBase):
    """
    A django-pipeline compiler that compiles SCSS to CSS using libsass. Unlike
    the default compiler provided by django-pipeline, this one can be run
    without any non-Python dependencies.
    """

    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith(('.scss', '.sass'))

    def compile_file(self, infile, outfile, outdated=False, force=False):
        source_sass = self.read_file(infile)
        compiled_css = sass.compile(
            string=source_sass,
            include_paths=self._include_paths(),
            custom_functions=self._custom_sass_functions(),
        )
        self.save_file(outfile, compiled_css)

    def _include_paths(self):
        return [
            os.path.join(path, 'css')
            for path
            in settings.STATICFILES_DIRS
        ]

    def _custom_sass_functions(self):
        return {
            'static_url': lambda path: self._static_url(path),
        }

    def _static_url(self, path):
        static_url = os.path.join(settings.STATIC_URL, path)
        return 'url(%s)' % static_url
