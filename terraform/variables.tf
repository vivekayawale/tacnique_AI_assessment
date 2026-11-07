variable "landlord_accounts" {
  type        = list(string)
  description = "Landlord account IDs whose media buckets are managed."
  default     = ["la-001", "la-002", "la-004"]
}
