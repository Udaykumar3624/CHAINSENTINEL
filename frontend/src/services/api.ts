import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to inject JWT Bearer token into headers
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('chainsentinel_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

// Interceptor to handle 401 Unauthorized responses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      if (!window.location.pathname.includes('/login')) {
        localStorage.removeItem('chainsentinel_token');
        localStorage.removeItem('chainsentinel_user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export interface UserAuthResponse {
  id: string;
  username: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: UserAuthResponse;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
  live_data_enabled: boolean;
  timestamp: string;
  disclaimer: string;
}

export interface KpiMetrics {
  total_transactions_analyzed: number;
  high_critical_alerts: number;
  open_cases: number;
  flagged_clusters: number;
}

export interface RiskDistribution {
  low: number;
  medium: number;
  high: number;
  critical: number;
}

export interface DashboardAlertItem {
  id: string;
  alert_code: string;
  title: string;
  subject_type: string;
  subject_id: string;
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  status: string;
  top_signal: string;
  created_at: string;
}

export interface ActivityTrendPoint {
  date: string;
  low_count: number;
  medium_count: number;
  high_count: number;
  critical_count: number;
}

export interface DemoScenarioItem {
  id: string;
  scenario_code: string;
  title: string;
  risk_level: string;
  expected_score: number;
  subject_type: string;
  subject_id: string;
  description: string;
  judging_story: string;
}

export interface DemoScenariosResponse {
  scenarios: DemoScenarioItem[];
  count: number;
  mode: string;
}

export interface SignalItem {
  code: string;
  title: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  score_contribution: number;
  explanation: string;
  observed_values: Record<string, any>;
  recommended_review_step: string;
}

export interface RiskDecomposition {
  rule_score: number;
  ml_score: number;
  graph_score: number;
}

export interface AnalysisResultResponse {
  subject_type: string;
  subject_id: string;
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  composite_risk_score?: number;
  risk_category?: string;
  rule_score?: number;
  ml_score?: number;
  graph_score?: number;
  confidence: number;
  score_decomposition: RiskDecomposition;
  triggered_indicators?: string[];
  feature_values?: Record<string, any>;
  evidence?: SignalItem[];
  signals: SignalItem[];
  recommended_action: string;
  data_source: string;
  is_ml_fallback?: boolean;
  disclaimer: string;
  analyzed_at: string;
}

export interface CsvDatasetSummary {
  total_records: number;
  unique_addresses: number;
  time_range_start?: string;
  time_range_end?: string;
  total_volume_btc: number;
  avg_transaction_amount_btc: number;
  median_transaction_amount_btc: number;
  missing_values_count: number;
  duplicate_records_count: number;
  scenario_distribution: Record<string, number>;
}

export interface CsvAnalysisSummaryItem {
  row_index: number;
  tx_hash: string;
  source_address: string;
  destination_address: string;
  amount_btc: number;
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  top_signal: string;
  in_degree?: number;
  out_degree?: number;
  pagerank?: number;
  has_cycle?: boolean;
  hop_distance?: number;
  data_source_label?: string;
}

export interface CsvAnalysisBatchResponse {
  filename: string;
  data_source_label?: string;
  total_rows_processed: number;
  summary?: CsvDatasetSummary;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  results: CsvAnalysisSummaryItem[];
  disclaimer: string;
}

export interface GraphNodeMetadata {
  in_degree: number;
  out_degree: number;
  pagerank: number;
  shortest_distance_to_flagged?: number;
  cluster_label?: string;
  tx_count?: number;
  volume_btc?: number;
  signals?: string[];
}

export interface CytoscapeNodeData {
  id: string;
  label: string;
  type: string;
  risk_level: 'low' | 'medium' | 'high' | 'critical' | 'unknown';
  risk_score: number;
  amount_btc?: number;
  metadata: GraphNodeMetadata;
}

export interface CytoscapeNodeWrapper {
  data: CytoscapeNodeData;
}

export interface CytoscapeEdgeData {
  id: string;
  source: string;
  target: string;
  txid: string;
  amount: number;
  timestamp: string;
  risk_level: string;
}

export interface CytoscapeEdgeWrapper {
  data: CytoscapeEdgeData;
}

export interface GraphMetricsSummary {
  total_nodes: number;
  total_edges: number;
  has_cycle: boolean;
  cycles_found: string[][];
  max_component_size: number;
  flagged_entities_count: number;
}

export interface GraphResponse {
  subject_type: string;
  subject_id: string;
  hops: number;
  nodes: CytoscapeNodeWrapper[];
  edges: CytoscapeEdgeWrapper[];
  metrics: GraphMetricsSummary;
  is_truncated: boolean;
  truncation_message?: string;
  disclaimer: string;
}

export interface AlertItem {
  id: string;
  alert_code: string;
  title: string;
  subject_type: string;
  subject_id: string;
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  status: 'new' | 'under_review' | 'resolved' | 'false_positive';
  top_signal: string;
  evidence: Record<string, any>;
  created_at: string;
}

export interface CaseNoteItem {
  id: string;
  case_id: string;
  author_name: string;
  note_text: string;
  created_at: string;
}

export interface AuditLogItem {
  id: string;
  action: string;
  actor_id: string;
  entity_type: string;
  entity_id: string;
  details?: Record<string, any>;
  created_at: string;
}

export interface CaseItem {
  id: string;
  case_number: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'in_progress' | 'closed';
  assigned_investigator: string;
  created_at: string;
  updated_at: string;
  linked_addresses: string[];
  linked_transactions: string[];
  notes: CaseNoteItem[];
  audit_logs: AuditLogItem[];
}

export interface GenerateDatasetRequest {
  num_records: number;
  seed: number;
  scenario_distribution?: Record<string, number>;
}

export interface GenerateDatasetResponse {
  dataset_id: string;
  filename: string;
  num_records: number;
  seed: number;
  file_size_bytes: number;
  created_at: string;
  disclaimer: string;
}

export interface ValidationErrorItem {
  row_index: number;
  field: string;
  error_type: string;
  message: string;
  value?: string;
}

export interface DatasetValidationReport {
  is_valid: boolean;
  total_rows_checked: number;
  error_count: number;
  errors: ValidationErrorItem[];
  warnings: string[];
}

export interface DatasetStatsSummary {
  total_transactions: number;
  normal_count: number;
  suspicious_count: number;
  total_volume_btc: number;
  avg_amount_btc: number;
  min_amount_btc: number;
  max_amount_btc: number;
  unique_inputs_count: number;
  unique_outputs_count: number;
  scenario_breakdown: Record<string, number>;
  label_breakdown: Record<string, number>;
}

export interface DatasetAnalysisResultItem {
  row_index: number;
  transaction_id: string;
  input_address: string;
  output_address: string;
  amount_btc: number;
  ground_truth_scenario: string;
  ground_truth_label: string;
  computed_risk_score: number;
  computed_risk_level: 'low' | 'medium' | 'high' | 'critical';
  top_signal: string;
}

export interface DatasetAnalysisResponse {
  dataset_id: string;
  filename: string;
  stats: DatasetStatsSummary;
  validation: DatasetValidationReport;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  results: DatasetAnalysisResultItem[];
  disclaimer: string;
}

export interface ActiveDatasetInfo {
  dataset_id: string;
  filename: string;
  data_source_type: string;
  data_source_label: string;
  row_count: number;
  analysis_status: string;
  created_at: string;
}

export interface DashboardSummaryResponse {
  kpis: KpiMetrics;
  risk_distribution: RiskDistribution;
  recent_alerts: DashboardAlertItem[];
  activity_trend: ActivityTrendPoint[];
  active_dataset?: ActiveDatasetInfo;
  disclaimer: string;
}

export const fetchBackendHealth = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>('/health');
  return response.data;
};

export const fetchDashboardSummary = async (): Promise<DashboardSummaryResponse> => {
  const response = await apiClient.get<DashboardSummaryResponse>('/dashboard/summary');
  return response.data;
};

export const resetActiveDataset = async (): Promise<DashboardSummaryResponse> => {
  const response = await apiClient.post<DashboardSummaryResponse>('/dashboard/reset');
  return response.data;
};

export const loadDemoDataset = async (): Promise<DashboardSummaryResponse> => {
  const response = await apiClient.post<DashboardSummaryResponse>('/dashboard/load-demo');
  return response.data;
};

export const fetchDemoScenarios = async (): Promise<DemoScenariosResponse> => {
  const response = await apiClient.get<DemoScenariosResponse>('/demo/scenarios');
  return response.data;
};

export const analyzeAddress = async (address: string): Promise<AnalysisResultResponse> => {
  const response = await apiClient.post<AnalysisResultResponse>('/analyze/address', { address });
  return response.data;
};

export const analyzeTransaction = async (txid: string): Promise<AnalysisResultResponse> => {
  const response = await apiClient.post<AnalysisResultResponse>('/analyze/transaction', { txid });
  return response.data;
};

export const analyzeCsv = async (file: File): Promise<CsvAnalysisBatchResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await apiClient.post<CsvAnalysisBatchResponse>('/analyze/csv', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const fetchEntityGraph = async (
  subjectType: string,
  subjectId: string,
  hops: number = 1,
  riskLevel: string = 'all',
  datasetId?: string
): Promise<GraphResponse> => {
  let url = `/graph/${subjectType}/${subjectId}?hops=${hops}&risk_level=${riskLevel}`;
  if (datasetId) url += `&dataset_id=${datasetId}`;
  const response = await apiClient.get<GraphResponse>(url);
  return response.data;
};

export const fetchAlerts = async (riskLevel?: string, status?: string): Promise<AlertItem[]> => {
  let url = '/alerts?limit=50';
  if (riskLevel && riskLevel !== 'all') url += `&risk_level=${riskLevel}`;
  if (status && status !== 'all') url += `&status=${status}`;
  const response = await apiClient.get<AlertItem[]>(url);
  return response.data;
};

export const updateAlertStatus = async (alertId: string, status: string): Promise<AlertItem> => {
  const response = await apiClient.patch<AlertItem>(`/alerts/${alertId}`, { status });
  return response.data;
};

export const fetchCases = async (status?: string, priority?: string): Promise<CaseItem[]> => {
  let url = '/cases';
  const params: string[] = [];
  if (status && status !== 'all') params.push(`status=${status}`);
  if (priority && priority !== 'all') params.push(`priority=${priority}`);
  if (params.length > 0) url += `?${params.join('&')}`;
  const response = await apiClient.get<CaseItem[]>(url);
  return response.data;
};

export const createCase = async (caseData: Partial<CaseItem>): Promise<CaseItem> => {
  const response = await apiClient.post<CaseItem>('/cases', caseData);
  return response.data;
};

export const addCaseNote = async (caseId: string, noteText: string, authorName: string = 'Investigator'): Promise<CaseNoteItem> => {
  const response = await apiClient.post<CaseNoteItem>(`/cases/${caseId}/notes`, {
    note_text: noteText,
    author_name: authorName,
  });
  return response.data;
};

export const generateSyntheticDataset = async (req: GenerateDatasetRequest): Promise<GenerateDatasetResponse> => {
  const response = await apiClient.post<GenerateDatasetResponse>('/dataset/generate', req);
  return response.data;
};

export const uploadDatasetFile = async (file: File): Promise<DatasetExplorerResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await apiClient.post<DatasetExplorerResponse>('/dataset/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const validateDatasetFile = async (file: File): Promise<DatasetValidationReport> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await apiClient.post<DatasetValidationReport>('/dataset/validate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getDatasetDownloadUrl = (datasetId: string): string => {
  return `${API_BASE_URL}/dataset/download/${datasetId}`;
};

export const getCasePdfUrl = (caseId: string): string => {
  return `${API_BASE_URL}/cases/${caseId}/report.pdf`;
};

export interface ConfusionMatrixInfo {
  tn: number;
  fp: number;
  fn: number;
  tp: number;
}

export interface HeldOutMetricsInfo {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
  test_samples: number;
  confusion_matrix: ConfusionMatrixInfo;
}

export interface ModelInfoResponse {
  model_name: string;
  model_version: string;
  is_trained: boolean;
  trained_at?: string;
  supervised_model: Record<string, any>;
  unsupervised_model: Record<string, any>;
  features_used: string[];
  feature_importances: Record<string, number>;
  held_out_metrics?: HeldOutMetricsInfo;
  preprocessing: string;
  train_test_split_ratio: string;
  random_seed: number;
  disclaimer: string;
}

export const fetchMlModelInfo = async (): Promise<ModelInfoResponse> => {
  const response = await apiClient.get<ModelInfoResponse>('/ml/info');
  return response.data;
};

export interface ExplorerSummary {
  total_transactions: number;
  unique_addresses: number;
  total_volume_btc: number;
  avg_transaction_amount_btc: number;
  time_range_start?: string;
  time_range_end?: string;
  missing_values_count: number;
  duplicate_records_count: number;
}

export interface EntityExtractedFeatures {
  address: string;
  amount_btc: number;
  inputs_count: number;
  outputs_count: number;
  fee_btc: number;
  time_delta_seconds: number;
  peel_steps: number;
  dormant_days: number;
  micro_tx_count: number;
  hop_distance: number;
  tx_count_24h: number;
  volume_btc_24h: number;
  in_degree: number;
  out_degree: number;
  pagerank: number;
  has_cycle: boolean;
}

export interface DatasetExplorerResponse {
  dataset_id: string;
  filename: string;
  data_source_label: string;
  data_source_type: string;
  summary: ExplorerSummary;
  scenario_distribution: Record<string, number>;
  transactions: DatasetAnalysisResultItem[];
  extracted_features: EntityExtractedFeatures[];
  disclaimer: string;
}

export const fetchDatasetExplorer = async (datasetId?: string): Promise<DatasetExplorerResponse> => {
  const url = datasetId ? `/dataset/explorer/${datasetId}` : '/dataset/explorer';
  const response = await apiClient.get<DatasetExplorerResponse>(url);
  return response.data;
};

export const loginUser = async (username: string, password: string): Promise<TokenResponse> => {
  const response = await apiClient.post<TokenResponse>('/auth/login', { username, password });
  return response.data;
};

export const logoutUser = async (): Promise<void> => {
  try {
    await apiClient.post('/auth/logout');
  } catch (err) {
    // Ignore error on logout call
  }
};

export const fetchCurrentUser = async (): Promise<UserAuthResponse> => {
  const response = await apiClient.get<UserAuthResponse>('/auth/me');
  return response.data;
};

