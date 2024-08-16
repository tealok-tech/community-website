import logging
from pathlib import Path

from lektor.context import get_ctx
from lektor.markdown import Markdown
from lektor.pluginsystem import Plugin
from lektor.types.base import Type


LOGGER = logging.getLogger(__name__)
# Stupid lektor doesn't actually use the logging system for Python
logging.basicConfig(level=logging.INFO)

class MarkdownFileType(Type):
	name = "markdown-file"	# ETA: explicit type name.	(The default is derived from the class name and would be "markdownfile" in this case.)

	widget = "hidden"	# This is the one part that might take some changes in the Lektor GUI code to support?

	def value_from_raw(self, __raw):
		LOGGER.info("Creating MarkdownFileType for %s", self.options)
		return MarkdownFileDescriptor(self.options)

class MarkdownFileDescriptor:
	def __init__(self, options):
		self.options = options

	def __get__(self, obj, type=None):
		LOGGER.info("get %s", obj)
		if obj is None:
			return self
		record_source_filename = next(obj.iter_source_filenames())
		record_source_dir = Path(record_source_filename).parent
		filename = self.options.get("file", "_contents.md")
		source_path = Path(record_source_dir, filename)

		try:
			source = source_path.read_text()
		except FileNotFoundError:
			source = self.options.get("default", "")
		return DepTrackingMarkdown(source, record=obj, field_options=self.options, source_path=source_path)

class DepTrackingMarkdown(Markdown):
	# XXX: might be better to use some pre-made proxy
	def __init__(self, source, record, field_options, source_path):
		LOGGER.info("Creating DepTrackingMarkdown")
		super().__init__(source, record, field_options)
		self.source_path = source_path

	def _Markdown__render(self):
		LOGGER.info("Rendering DepTrackingMarkdown")
		# declare dependency on source_path any time rendered result is accessed
		ctx = get_ctx()
		if ctx is not None:
			ctx.record_dependency(str(self.source_path))
		return super()._Markdown__render()


class MarkdownFromFilePlugin(Plugin):
	name = u'MarkdownFile'
	description = "Include whole markdown files as the body of posts"


	def on_setup_env(self, **extra):
		print("GOTCHA")
		LOGGER.info("HEY")
		self.env.add_type(MarkdownFileType)
