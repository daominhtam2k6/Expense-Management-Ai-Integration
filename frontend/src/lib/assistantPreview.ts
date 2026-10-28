import { toString } from "mdast-util-to-string";
import remarkGfm from "remark-gfm";
import remarkParse from "remark-parse";
import { unified } from "unified";
import type { Nodes } from "mdast";

const parser = unified().use(remarkParse).use(remarkGfm);

function readableText(node: Nodes): string {
  if (node.type === "html") return "";
  if ("children" in node && !["paragraph", "heading", "link", "emphasis", "strong", "delete"].includes(node.type)) {
    return node.children.map((child) => readableText(child)).join(" ");
  }
  return toString(node, { includeHtml: false });
}

/** Display-only: saved responses and numeric values remain untouched. */
export function assistantPreview(markdown: string): string {
  return readableText(parser.parse(markdown)).replace(/\s+/g, " ").trim();
}
