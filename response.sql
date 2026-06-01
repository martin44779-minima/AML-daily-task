-- public.dify_call_results definition

-- Drop table

-- DROP TABLE public.dify_call_results;

CREATE TABLE public.dify_call_results (
	id serial4 NOT NULL,
	task_id int4 NULL,
	upload_api_response json NULL,
	run_response json NULL,
	parsed_result json NULL,
	Reserved1 json NULL,
	Reserved2 json NULL,
	Reserved3 json NULL,
	Reserved4 json NULL,
	Reserved5 json NULL,
	Reserved6 json NULL,
	Reserved7 json NULL,
	Reserved8 json null,
	execution_time timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	status varchar(50) DEFAULT 'pending'::character varying NULL,
	CONSTRAINT dify_call_results_pkey PRIMARY KEY (id)
);


-- public.dify_call_results foreign keys

ALTER TABLE public.dify_call_results ADD CONSTRAINT dify_call_results_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task_configs(id);