import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function AssistantMessage({ content }: { content: string }) {
  return (
    <div className="assistant-answer">
      <Markdown
        remarkPlugins={[remarkGfm]}
        skipHtml
        components={{
          // Generated answers must not load remote images or tracking pixels.
          img: ({ alt }) => <span>{alt}</span>,
          a: ({ href, children }) => {
            if (!href) return <span>{children}</span>;
            return <a href={href} target="_blank" rel="noopener noreferrer">{children}</a>;
          },
          h1: ({ children }) => <h3>{children}</h3>,
          h2: ({ children }) => <h3>{children}</h3>,
          table: ({ children }) => (
            <div className="assistant-answer__table" role="region" aria-label="Bảng trong câu trả lời AI" tabIndex={0}>
              <table>{children}</table>
            </div>
          ),
          pre: ({ children }) => <pre tabIndex={0} aria-label="Đoạn mã trong câu trả lời AI">{children}</pre>,
        }}
      >
        {content}
      </Markdown>
    </div>
  );
}
