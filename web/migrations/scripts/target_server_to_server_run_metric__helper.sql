-- Script to convert target_server_cpu, target_server_memory, and
-- target_server_load into server_run_metric.
--
-- NOTICE: do not run this unless you know what you are doing!
--
-- create new 'server_run_metric', get its id and create the
-- 'target_serverrunmetric_testresults' association between it
-- and the testresult.
DO language plpgsql $$
DECLARE
  rec test_result%rowtype;
  cpu_avg_metric_id integer;
  memory_free_avg_metric_id integer;
  load_avg_metric_id integer;
  srm_id integer;
begin
  select id into cpu_avg_metric_id from run_metric where name = 'CPU Avg';
  select id into memory_free_avg_metric_id from run_metric where name = 'Mem Free Avg';
  select id into load_avg_metric_id from run_metric where name = 'Load Avg';

  FOR rec IN SELECT * FROM test_result where target_server_cpu is not null
  LOOP
    srm_id = null;
    RAISE NOTICE '%', rec.id || '-' || rec.test_date;
    --create 'cpu avg' record
    insert into server_run_metric (run_metric_id, value) values (cpu_avg_metric_id, rec.target_server_cpu) RETURNING id into srm_id;
    insert into target_serverrunmetric_testresults (testresult_id, server_run_metric_id) values (rec.id, srm_id);
    RAISE NOTICE '%', 'created srm for cpu avg with id: ' || srm_id;
  END LOOP;

  FOR rec IN SELECT * FROM test_result where target_server_memory is not null
  LOOP
    srm_id = null;
    RAISE NOTICE '%', rec.id || '-' || rec.test_date;
    --RAISE NOTICE '%', 'cpu avg metric id=' || cpu_avg_metric_id;
    --create 'free mem avg' record
    insert into server_run_metric (run_metric_id, value) values (memory_free_avg_metric_id, rec.target_server_memory) RETURNING id into srm_id;
    insert into target_serverrunmetric_testresults (testresult_id, server_run_metric_id) values (rec.id, srm_id);
    RAISE NOTICE '%', 'created srm for free mem avg with id: ' || srm_id;
  END LOOP;

  FOR rec IN SELECT * FROM test_result where target_server_load is not null
  LOOP
    srm_id = null;
    RAISE NOTICE '%', rec.id || '-' || rec.test_date;
    --RAISE NOTICE '%', 'cpu avg metric id=' || cpu_avg_metric_id;
    --create 'load avg' record
    insert into server_run_metric (run_metric_id, value) values (load_avg_metric_id, rec.target_server_load) RETURNING id into srm_id;
    insert into target_serverrunmetric_testresults (testresult_id, server_run_metric_id) values (rec.id, srm_id);
    RAISE NOTICE '%', 'created srm for load avg with id: ' || srm_id;
  END LOOP;
END;
$$;
