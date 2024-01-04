CREATE TABLE public.imported_documents (
	id              serial PRIMARY KEY,
	file_name       VARCHAR(250) UNIQUE NOT NULL,
	xml             XML NOT NULL,
	deleted_at      TIMESTAMP,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.converted_documents (
    id              serial PRIMARY KEY,
    file_name       VARCHAR(250) UNIQUE NOT NULL,
    file_size       BIGINT NOT NULL,
    csv_path        TEXT  NOT NULL,
    deleted_at      TIMESTAMP,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);
