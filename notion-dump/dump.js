const { Client } = require("@notionhq/client");
const { NotionToMarkdown } = require("notion-to-md");

const notion = new Client({
  auth: process.env.NOTION_TOKEN,
});

const n2m = new NotionToMarkdown({ notionClient: notion });

const fetchPage = async (id) => {
  const mdblocks = await n2m.pageToMarkdown(id);
  const mdString = n2m.toMarkdownString(mdblocks);
  return mdString.parent;
};

if (require.main === module && process.argv.length > 2) {
  const id = process.argv[2];
  fetchPage(id).then(console.log).catch(console.log);
}
