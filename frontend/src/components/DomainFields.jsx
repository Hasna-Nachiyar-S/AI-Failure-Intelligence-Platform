import { DOMAIN_FIELDS } from "../config/domains";

/** Render a domain's input fields from metadata rather than repeating JSX. */
export default function DomainFields({ domain, values, onChange }) {
  return DOMAIN_FIELDS[domain].map(({ key, label, type = "text", ...constraints }) => (
    <label className="field" key={key}>
      <span>{label}</span>
      <input
        type={type}
        value={values[key] ?? ""}
        {...constraints}
        onChange={(event) =>
          onChange(key, type === "number" ? Number(event.target.value) : event.target.value)
        }
      />
    </label>
  ));
}
